from src.ReversiGUI import ReversiGUI
from models.cpu.util import find_valid_moves


# コーナー優先戦略：最も多くの石をひっくり返せる手を選び、コーナーとその近傍の優先度を調整
def cpu_lv2(board, player_num):
    # 置ける手を探す
    valid_moves = find_valid_moves(board, player_num)  # 有効な手を取得
    if valid_moves == []:  # 有効な手がない場合
        return []  # 空のリストを返す
    best_move = None  # 最良の手を初期化
    max_flipped = -1  # 最大でひっくり返せるコマの数を初期化
    for move in valid_moves:  # 各有効な手について
        x, y = move  # 手の座標を取得
        temp_board = [row[:] for row in board]  # ボードのコピーを作成
        flipped_count = 0  # ひっくり返せるコマの数を初期化
        # ひっくり返す方向を定義
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        if (x == 1 or x == 8) and (y == 1 or y == 8):
            flipped_count += 100  # コーナーを優先して取る
        elif (x == 2 or x == 7) and (y == 2 or y == 7):
            flipped_count -= 100  # コーナーの斜め前を避ける

        for dx, dy in directions:  # 各方向について
            nx, ny = x + dx, y + dy  # 次の座標を計算
            temp_flipped = 0  # 一時的にひっくり返せるコマの数を初期化
            # ボードの範囲内で、相手のコマが続く限り
            while 1 <= nx <= 8 and 1 <= ny <= 8 and temp_board[ny][nx] == -player_num:
                temp_flipped += 1  # ひっくり返せるコマをカウント
                nx += dx  # 次の座標に移動
                ny += dy  # 次の座標に移動
            # 最後に自分のコマがある場合
            if 1 <= nx <= 8 and 1 <= ny <= 8 and temp_board[ny][nx] == player_num:
                flipped_count += temp_flipped  # ひっくり返せるコマの合計に加算
        # 最大のひっくり返せるコマ数を更新
        if flipped_count > max_flipped:
            max_flipped = flipped_count  # 最大値を更新
            best_move = move  # 最良の手を更新

    return best_move  # 最良の手を返す
