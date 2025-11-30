from src.ReversiGUI import ReversiGUI
from cpu.util import find_valid_moves

# fmt: off  # Disable Black formatting for the following weights array
# yapf: disable  # Disable YAPF
# autopep8: off  # Hint for some tools

# どのマスが有利かを示す重み付け配列
weights = [
    [0,   0,   0,  0,  0,  0,  0,   0,   0, 0],
    [0, 100, -20, 10,  5,  5, 10, -20, 100, 0],
    [0, -20, -50, -2, -2, -2, -2, -50, -20, 0],
    [0,  10,  -2, -1, -1, -1, -1,  -2,  10, 0],
    [0,   5,  -2, -1, -1, -1, -1,  -2,   5, 0],
    [0,   5,  -2, -1, -1, -1, -1,  -2,   5, 0],
    [0,  10,  -2, -1, -1, -1, -1,  -2,  10, 0],
    [0, -20, -50, -2, -2, -2, -2, -50, -20, 0],
    [0, 100, -20, 10,  5,  5, 10, -20, 100, 0],
    [0,   0,   0,  0,  0,  0,  0,   0,   0, 0],
]

# おまじない
# fmt: on  # Disable Black formatting for the following weights array
# yapf: enable  # Disable YAPF
# autopep8: on  # Hint for some tools


# 各位置の重み付けに基づいて手を選ぶモデル
def cpu_lv3(board, player_num):
    # 置ける手を探す
    valid_moves = find_valid_moves(board, player_num)  # 有効な手を取得
    if valid_moves == []:  # 有効な手がない場合
        return []  # 空のリストを返す

    best_move = None  # 最良の手を初期化
    max_score = -10**9  # 最大でひっくり返せるコマの数を初期化
    for move in valid_moves:  # 各有効な手について
        x, y = move  # 手の座標を取得
        temp_board = [row[:] for row in board]  # ボードのコピーを作成
        score = 0  # ひっくり返せるコマの数を初期化
        # ひっくり返す方向を定義
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1),
                      (1, 0), (1, 1)]

        score = weights[x][y]  # 置く位置の重みを加算
        for dx, dy in directions:  # 各方向について
            nx, ny = x + dx, y + dy  # 次の座標を計算
            temp_score = 0  # 一時的にひっくり返せるコマの数を初期化
            # ボードの範囲内で、相手のコマが続く限り
            while 1 <= nx <= 8 and 1 <= ny <= 8 and temp_board[ny][nx] == -player_num:
                temp_score += weights[nx][ny]  # ひっくり返せるコマのスコアを加算
                nx += dx  # 次の座標に移動
                ny += dy  # 次の座標に移動
            # 最後に自分のコマがある場合
            if 1 <= nx <= 8 and 1 <= ny <= 8 and temp_board[ny][nx] == player_num:
                score += temp_score  # ひっくり返せるコマの合計に加算
        # 最大のひっくり返せるコマ数を更新
        if score > max_score:
            max_score = score  # 最大値を更新
            best_move = move  # 最良の手を更新

    return best_move  # 最良の手を返す
