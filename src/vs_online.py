"""LAN内でモデルを交換して、双方のPCで同じ対局を実行する。

``battle.py`` で対戦相手に「online」を選ぶと ``run_online_match`` が呼ばれる。
``model.py`` の ``cpu_algorithm`` を編集してから実行する。通信するのは
対局開始時のモデル交換だけで、対局そのものは各PC上で実行される。
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import random
import select
import secrets
import socket
import struct
import sys
import time
import types
from pathlib import Path
from typing import Callable

import questionary

from src.ReversiGUI import ReversiGUI

PORT = 54231
DISCOVERY_PORT = 54230
MAX_MESSAGE_SIZE = 512 * 1024
PROTOCOL = "aic-reversi-1"
Algorithm = Callable[[list[list[int]], int], list[int]]


class ProtocolError(Exception):
    pass


def _send(sock: socket.socket, data: dict) -> None:
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    if len(body) > MAX_MESSAGE_SIZE:
        raise ProtocolError("送信するモデルが大きすぎます")
    sock.sendall(struct.pack("!I", len(body)) + body)


def _receive(sock: socket.socket) -> dict:
    header = _read_exactly(sock, 4)
    size = struct.unpack("!I", header)[0]
    if size > MAX_MESSAGE_SIZE:
        raise ProtocolError("受信データが大きすぎます")
    try:
        data = json.loads(_read_exactly(sock, size).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("受信データを読めません") from exc
    if not isinstance(data, dict):
        raise ProtocolError("不正な受信データです")
    return data


def _read_exactly(sock: socket.socket, size: int) -> bytes:
    chunks = bytearray()
    while len(chunks) < size:
        chunk = sock.recv(size - len(chunks))
        if not chunk:
            raise ProtocolError("接続が切れました")
        chunks.extend(chunk)
    return bytes(chunks)


def _proof(password: str, role: bytes, nonce: bytes) -> str:
    return hmac.new(password.encode("utf-8"), role + nonce, hashlib.sha256).hexdigest()


def _authenticate_host(sock: socket.socket, password: str) -> bool:
    host_nonce = secrets.token_bytes(32)
    _send(
        sock,
        {
            "type": "hello",
            "protocol": PROTOCOL,
            "nonce": base64.b64encode(host_nonce).decode("ascii"),
        },
    )
    reply = _receive(sock)
    try:
        guest_nonce = base64.b64decode(reply["nonce"], validate=True)
        guest_proof = reply["proof"]
    except (KeyError, TypeError, ValueError) as exc:
        raise ProtocolError("認証データが不正です") from exc

    ok = (
        reply.get("type") == "auth"
        and len(guest_nonce) == 32
        and isinstance(guest_proof, str)
        and hmac.compare_digest(guest_proof, _proof(password, b"guest", host_nonce))
    )
    _send(
        sock,
        {
            "type": "auth_result",
            "ok": ok,
            "proof": _proof(password, b"host", guest_nonce) if ok else "",
        },
    )
    return ok


def _authenticate_guest(sock: socket.socket, password: str) -> None:
    hello = _receive(sock)
    try:
        host_nonce = base64.b64decode(hello["nonce"], validate=True)
    except (KeyError, TypeError, ValueError) as exc:
        raise ProtocolError("ホストの認証データが不正です") from exc
    if hello.get("type") != "hello" or hello.get("protocol") != PROTOCOL:
        raise ProtocolError("相手のvs_online.pyと通信方式が一致しません")

    guest_nonce = secrets.token_bytes(32)
    _send(
        sock,
        {
            "type": "auth",
            "nonce": base64.b64encode(guest_nonce).decode("ascii"),
            "proof": _proof(password, b"guest", host_nonce),
        },
    )
    result = _receive(sock)
    expected = _proof(password, b"host", guest_nonce)
    if not result.get("ok"):
        raise ProtocolError("合言葉が違います")
    if not hmac.compare_digest(str(result.get("proof", "")), expected):
        raise ProtocolError("ホストを認証できません")


def _model_message(name: str, source: str) -> dict:
    return {"type": "model", "name": name[:40], "source": source}


def _parse_model(data: dict) -> tuple[str, str]:
    name, source = data.get("name"), data.get("source")
    if (
        data.get("type") != "model"
        or not isinstance(name, str)
        or not isinstance(source, str)
    ):
        raise ProtocolError("モデルデータが不正です")
    if not name.strip() or len(source.encode("utf-8")) > MAX_MESSAGE_SIZE:
        raise ProtocolError("モデル名またはサイズが不正です")
    return name, source


def _room_id(password: str) -> str:
    """探索時に合言葉そのものを流さないための短い識別子。"""
    value = f"{PROTOCOL}\0{password}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()[:24]


def _discovery_listener() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("0.0.0.0", DISCOVERY_PORT))
    except Exception:
        sock.close()
        raise
    return sock


def _answer_discovery(sock: socket.socket, password: str, port: int) -> None:
    try:
        packet, address = sock.recvfrom(2048)
        request = json.loads(packet.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return
    room = _room_id(password)
    if request != {"type": "discover", "protocol": PROTOCOL, "room": room}:
        return
    response = json.dumps(
        {"type": "room", "protocol": PROTOCOL, "room": room, "port": port}
    ).encode("utf-8")
    sock.sendto(response, address)


def discover_room(password: str, timeout: float = 5) -> tuple[str, int] | None:
    """LANへ問い合わせ、合言葉が一致するホストの(IP, port)を返す。"""
    room = _room_id(password)
    request = json.dumps(
        {"type": "discover", "protocol": PROTOCOL, "room": room}
    ).encode("utf-8")
    deadline = time.monotonic() + timeout
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while time.monotonic() < deadline:
            try:
                sock.sendto(request, ("255.255.255.255", DISCOVERY_PORT))
            except OSError:
                return None
            sock.settimeout(min(1, max(0.1, deadline - time.monotonic())))
            try:
                packet, address = sock.recvfrom(2048)
                response = json.loads(packet.decode("utf-8"))
            except socket.timeout:
                continue
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            if not isinstance(response, dict):
                continue
            port = response.get("port")
            if (
                response.get("type") == "room"
                and response.get("protocol") == PROTOCOL
                and response.get("room") == room
                and isinstance(port, int)
                and 1 <= port <= 65535
            ):
                return address[0], port
    return None


def create_room(password: str, name: str, source: str, bind: str, port: int):
    """参加者を1人待ち、(相手名, 相手ソース, 乱数seed)を返す。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((bind, port))
        server.listen()
        try:
            discovery = _discovery_listener()
        except OSError as exc:
            discovery = None
            print(f"自動探索を開始できませんでした: {exc}")

        print("ルームを作成しました。参加者は同じ合言葉を入力してください。")
        print(f"自動探索できない場合の接続先: {_local_ip()}:{port}")
        print("参加者を待っています（終了: Ctrl+C）")

        try:
            while True:
                sockets = [server]
                if discovery is not None:
                    sockets.append(discovery)
                readable, _, _ = select.select(sockets, [], [])
                if discovery is not None and discovery in readable:
                    _answer_discovery(discovery, password, port)
                    continue

                conn, address = server.accept()
                with conn:
                    conn.settimeout(15)
                    try:
                        if not _authenticate_host(conn, password):
                            print(f"認証失敗: {address[0]}")
                            continue
                        guest_name, guest_source = _parse_model(_receive(conn))
                        seed = secrets.randbits(64)
                        message = _model_message(name, source)
                        message["seed"] = seed
                        _send(conn, message)
                        print(f"接続しました: {guest_name} ({address[0]})")
                        return guest_name, guest_source, seed
                    except (OSError, ProtocolError) as exc:
                        print(f"接続エラー ({address[0]}): {exc}")
        finally:
            if discovery is not None:
                discovery.close()


def join_room(host: str, password: str, name: str, source: str, port: int):
    """ホストへ参加し、(相手名, 相手ソース, 乱数seed)を返す。"""
    with socket.create_connection((host, port), timeout=10) as sock:
        sock.settimeout(15)
        _authenticate_guest(sock, password)
        _send(sock, _model_message(name, source))
        data = _receive(sock)
        host_name, host_source = _parse_model(data)
        seed = data.get("seed")
        if not isinstance(seed, int):
            raise ProtocolError("対局データが不正です")
        print(f"接続しました: {host_name} ({host})")
        return host_name, host_source, seed


def _load_algorithm(source: str, label: str) -> Algorithm:
    """交換したファイルを独立したモジュールとしてローカル実行する。"""
    module_name = "_online_model_" + hashlib.sha256(source.encode()).hexdigest()[:12]
    module = types.ModuleType(module_name)
    module.__file__ = f"<{label}>"
    try:
        exec(compile(source, module.__file__, "exec"), module.__dict__)
    except Exception as exc:
        raise ProtocolError(f"{label}の読み込みに失敗しました: {exc}") from exc
    algorithm = getattr(module, "cpu_algorithm", None)
    if not callable(algorithm):
        raise ProtocolError(f"{label}にcpu_algorithm関数がありません")
    return algorithm


def _local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.connect(("192.0.2.1", 80))
            return sock.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())


def _ask(question):
    answer = question.ask()
    if answer is None:
        raise ProtocolError("操作を中止しました")
    return answer


def _setup() -> tuple[str, str, str]:
    mode = _ask(
        questionary.select(
            "オンライン対戦",
            choices=[
                questionary.Choice("ルームを作成する（黒）", value="create"),
                questionary.Choice("ルームに参加する（白）", value="join"),
            ],
        )
    )
    name = _ask(questionary.text("モデル名:")).strip()
    if not name:
        raise ProtocolError("モデル名を空にはできません")

    password = _ask(questionary.password("合言葉:"))
    if not password:
        raise ProtocolError("合言葉を空にはできません")
    if mode == "create":
        confirmation = _ask(questionary.password("合言葉（確認）:"))
        if password != confirmation:
            raise ProtocolError("合言葉が一致しません")
    return mode, name, password


def _resolve_host(password: str) -> tuple[str, int]:
    """自動探索を試み、失敗したら手動入力にフォールバックする。"""
    print("同じ合言葉のルームを探しています...")
    room = discover_room(password)
    if room is not None:
        return room
    print("ルームを自動発見できませんでした。")
    host = _ask(questionary.text("ホストのIPアドレス:")).strip()
    if not host:
        raise ProtocolError("ホストのIPアドレスを入力してください")
    return host, PORT


def run_online_match() -> None:
    """battle.pyから呼び出すエントリポイント。"""
    try:
        _play()
    except (OSError, ProtocolError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _play() -> None:
    mode, name, password = _setup()
    source = (Path(__file__).resolve().parent.parent / "model.py").read_text(
        encoding="utf-8"
    )
    print(
        "注意: 接続相手のPythonコードをこのPC上で実行します。信頼できる相手だけと接続してください。"
    )

    if mode == "create":
        rival_name, rival_source, seed = create_room(
            password, name, source, "0.0.0.0", PORT
        )
        black, white = (name, source), (rival_name, rival_source)
    else:
        host, port = _resolve_host(password)
        rival_name, rival_source, seed = join_room(
            host, password, name, source, port
        )
        black, white = (rival_name, rival_source), (name, source)

    # 両端で同じ順序・seedからモデルを読み込み、同じ対局を再現する。
    random.seed(seed)
    (black_name, black_source), (white_name, white_source) = black, white
    app = ReversiGUI(
        first_algorithm=(_load_algorithm(black_source, black_name), black_name),
        second_algorithm=(_load_algorithm(white_source, white_name), white_name),
    )
    app.gui.mainloop()
