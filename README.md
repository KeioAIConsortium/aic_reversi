# <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" alt="Python" width="20" /> aic_reversi

リバーシ（オセロ）の CPU アルゴリズムを実装し、GUI 上で対戦できる教材リポジトリです。
基本的には [`model.py`](model.py) の `cpu_algorithm` を書き換えるだけで、人間・内蔵 CPU・過去の受講生モデル・LAN 上の相手と対戦できます。

![リバーシ画面](assets/image.png)

## クイックスタート

### 1. `uv` をインストールする

```sh
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. リポジトリを取得して依存関係をインストールする

```sh
git clone https://github.com/KeioAIConsortium/aic_reversi.git
cd aic_reversi
uv sync
```

このプロジェクトでは Python 3.13.6 を使用します。`uv sync` を実行すると、必要な Python とパッケージが用意されます。

### 3. 対戦を起動する

```sh
uv run battle.py
```

表示されたメニューから対戦相手を選び、Enter キーで決定します。自作 CPU は常に黒（先手）、選んだ相手は白（後手）です。`human` を選んだ場合は、白の手番で盤面をクリックして石を置きます。

対戦相手をコマンドから直接指定することもできます。

```sh
uv run battle.py --model_name human
uv run battle.py --model_name lv5
uv run battle.py --model_name student_best
```

指定できる名前は `human`、`lv0`〜`lv5`、`student_best`、`alphabeta`、`online` です。

> [!NOTE]
> GUI には `tkinter` が必要です。ウィンドウが表示されない場合は、`tkinter` を利用できる Python 環境か確認してください。

## CPU アルゴリズムを実装する

編集するファイルは [`model.py`](model.py) です。`cpu_algorithm(board, player_num)` が次の一手を返すように実装します。

```python
from src.ReversiGUI import ReversiGUI


def cpu_algorithm(board, player_num):
    valid_moves = []
    for x in range(1, 9):
        for y in range(1, 9):
            if ReversiGUI.validate_reversible(board, player_num, x, y):
                valid_moves.append([x, y])

    if valid_moves:
        return valid_moves[0]
    return []
```

- `board` は外周を含む 10 × 10 の二次元リストです。盤面として使う座標は `1`〜`8` です。
- マスを参照するときは `board[y][x]` を使います。
- `player_num` は黒なら `1`、白なら `-1` です。
- 石を置ける場合は座標を `[x, y]` のリストで返します。
- 石を置ける場所がない場合は空のリスト `[]` を返します。
- `ReversiGUI.validate_reversible(board, player_num, x, y)` で、その座標に石を置けるか判定できます。

戻り値が不正な場合、その手番はパスとして扱われます。

## 対戦相手

| 名前 | 内容 |
| --- | --- |
| `human` | 人間が GUI をクリックして対戦 |
| `lv0` | ランダムに手を選択 |
| `lv1` | 最も多くの石をひっくり返せる手を選択 |
| `lv2` | コーナーを優先 |
| `lv3` | 位置の重み付けに基づいて選択 |
| `lv4` | 以前の授業で作成されたモデル |
| `lv5` | αβ法で手を探索 |
| `student_best` | 受講生が作成した `spring_2026` のモデル |
| `alphabeta` | ビットボードを使った αβ法のモデル |
| `online` | LAN 上の相手とモデルを交換して対戦 |

## LAN 対戦

同じ LAN に接続した 2 台の PC で、それぞれ次を実行します。

```sh
uv run battle.py --model_name online
```

1. 一方が「ルームを作成する（黒）」を選び、モデル名と合言葉を入力します。
2. もう一方が「ルームに参加する（白）」を選び、同じ合言葉を入力します。
3. ルームが自動で見つからない場合は、作成側に表示された IP アドレスを参加側へ入力します。

対局開始時に、双方の [`model.py`](model.py) を交換します。通信後は両方の PC で同じ対局を実行するため、途中の各着手は通信しません。

> [!WARNING]
> LAN 対戦では、受信した相手の Python コードを自分の PC 上で実行します。信頼できる相手とのみ接続し、合言葉を共有してください。

自動探索では UDP `54230`、対戦接続では TCP `54231` を使用します。OS やネットワークのファイアウォールで接続できない場合は、これらのポートを確認してください。

## ディレクトリ構成

```text
aic_reversi/
├── assets/
│   └── image.png                 # README の画面例
├── models/
│   ├── alphabeta/                # ビットボード版 αβ法モデル
│   ├── cpu/                      # lv0〜lv5 の内蔵 CPU
│   ├── spring_2025/              # 2025年春の大会モデル
│   └── spring_2026/              # 2026年春の大会モデル
├── src/
│   ├── ReversiGUI.py             # 盤面・ルール・GUI
│   └── vs_online.py              # LAN 対戦処理
├── battle.py                     # 対戦のエントリーポイント
├── model.py                      # 自作 CPU の編集箇所
├── pyproject.toml                # Python・依存関係の設定
└── uv.lock                       # 依存関係のロックファイル
```

## 過去の大会

| 開催 | 概要 | 結果 |
| --- | --- | --- |
| `🌸 spring_2025` | 高校3年生向け Python 初級講座で CPU 実装対戦 | `team a` 優勝 |
| `🍧 aicdays_2025` | 中高生向け講座（Python 初級 / GAS × Python 中上級） | 通信対戦実装まで実施 |
| `🌸 spring_2026` | 高校3年生向け Python 初級講座で CPU 実装対戦 | `team 3校合同` が 2025年モデル超え（@Suzu-Yasu） |
