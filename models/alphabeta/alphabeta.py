from src.ReversiGUI import ReversiGUI
from models.cpu import cpu_lv5

"""
ビットボード表現 × 静的評価関数付きアルファベータ探索によるオセロAI

- 盤面は64bit整数2つ（自分の石 player_bb, 相手の石 opponent_bb）で表すビットボード。
  ビット i (0〜63) は x = i % 8, y = i // 8 のマス（本プロジェクトの内部座標では x+1, y+1）に対応する。
- 探索は「手番から見たスコア」を返す負了法（ネガマックス）＋アルファベータ枝刈りで行う。
"""

FULL = 0xFFFFFFFFFFFFFFFF
EDGE_MASK = 0x7E7E7E7E7E7E7E7E  # 左右端の列を除いたマスク（横・斜め方向のはみ出し防止）
DIRECTIONS = [1, -1, 8, -8, 7, -7, 9, -9]  # 右, 左, 下, 上, 左下, 右上, 右下, 左上

# 位置ごとの重み（角を高評価、角の隣は低評価）
WEIGHTS = [
    100, -20, 10, 5, 5, 10, -20, 100,
    -20, -50, -2, -2, -2, -2, -50, -20,
    10, -2, -1, -1, -1, -1, -2, 10,
    5, -2, -1, -1, -1, -1, -2, 5,
    5, -2, -1, -1, -1, -1, -2, 5,
    10, -2, -1, -1, -1, -1, -2, 10,
    -20, -50, -2, -2, -2, -2, -50, -20,
    100, -20, 10, 5, 5, 10, -20, 100,
]


def _shift(bb, d):
    """ビットボードを d マス分シフトする（正なら盤面上で+方向、負なら-方向）"""
    if d > 0:
        return (bb << d) & FULL
    return bb >> (-d)


def _dir_mask(d, opponent_bb):
    """方向 d へ辿るときの、はみ出し防止マスクを適用した相手石ビットボード"""
    return opponent_bb if d in (8, -8) else opponent_bb & EDGE_MASK


def board_to_bitboard(board, player_num):
    """本プロジェクト共通の10x10盤面を (自分, 相手) のビットボードに変換する"""
    player_bb = opponent_bb = 0
    for y in range(1, 9):
        for x in range(1, 9):
            i = (y - 1) * 8 + (x - 1)
            if board[y][x] == player_num:
                player_bb |= 1 << i
            elif board[y][x] == -player_num:
                opponent_bb |= 1 << i
    return player_bb, opponent_bb


def legal_moves(player_bb, opponent_bb):
    """置ける場所をビットが立った状態で返す（1マス=1ビット）"""
    empty = ~(player_bb | opponent_bb) & FULL
    moves = 0
    for d in DIRECTIONS:
        mask = _dir_mask(d, opponent_bb)
        flip = mask & _shift(player_bb, d)
        for _ in range(5):  # 盤面の1辺(8マス)を辿りきるまで繰り返す
            flip |= mask & _shift(flip, d)
        moves |= _shift(flip, d)
    return moves & empty


def apply_move(player_bb, opponent_bb, move_bit):
    """1手 move_bit を打った後の (自分, 相手) ビットボードを返す"""
    flips = 0
    for d in DIRECTIONS:
        mask = _dir_mask(d, opponent_bb)
        line = mask & _shift(move_bit, d)
        for _ in range(5):
            line |= mask & _shift(line, d)
        if _shift(line, d) & player_bb:  # 自分の石で挟めている方向だけ確定
            flips |= line
    return player_bb | move_bit | flips, opponent_bb & ~flips


def move_list(moves_bb):
    """ビットボードを (x, y) 座標（1〜8）のリストに変換する"""
    return [(i % 8 + 1, i // 8 + 1) for i in range(64) if moves_bb & (1 << i)]


def evaluate(player_bb, opponent_bb):
    """静的評価関数（手番側から見たスコア）：位置の重み差＋石数差＋着手可能数差"""
    pos_score = sum(
        WEIGHTS[i] if player_bb & (1 << i) else -WEIGHTS[i] if opponent_bb & (1 << i) else 0
        for i in range(64)
    )
    disc_diff = bin(player_bb).count("1") - bin(opponent_bb).count("1")
    mobility = bin(legal_moves(player_bb, opponent_bb)).count("1") - bin(
        legal_moves(opponent_bb, player_bb)
    ).count("1")
    return pos_score + disc_diff + 10 * mobility


def negamax(player_bb, opponent_bb, depth, alpha, beta):
    """アルファベータ法（負了法）：手番側(player_bb)から見たスコアを返す"""
    moves = legal_moves(player_bb, opponent_bb)

    if depth == 0:
        return evaluate(player_bb, opponent_bb)

    if moves == 0:
        if legal_moves(opponent_bb, player_bb) == 0:
            return evaluate(player_bb, opponent_bb)  # 両者パス→終局
        return -negamax(opponent_bb, player_bb, depth - 1, -beta, -alpha)  # 自分だけパス

    best = -10**9
    for x, y in move_list(moves):
        i = (y - 1) * 8 + (x - 1)
        new_player, new_opponent = apply_move(player_bb, opponent_bb, 1 << i)
        score = -negamax(new_opponent, new_player, depth - 1, -beta, -alpha)
        best = max(best, score)
        alpha = max(alpha, best)
        if alpha >= beta:  # 枝刈り
            break
    return best


def cpu_algorithm(board, player_num, depth=4):
    """
    ビットボード×アルファベータ探索で最善手を選ぶ関数

    引数:
    - board: 10x10の2次元リスト形式の盤面。
    - player_num: 現在のプレイヤーの番号（1または-1）。
    - depth: 探索の深さ（デフォルト4手先）。

    返り値:
    - 最善手の座標 [x, y]。置ける手が無い場合は空リスト。
    """
    player_bb, opponent_bb = board_to_bitboard(board, player_num)
    moves = move_list(legal_moves(player_bb, opponent_bb))
    if not moves:
        return []

    best_move, best_score = moves[0], -10**9
    alpha, beta = -10**9, 10**9
    for x, y in moves:
        i = (y - 1) * 8 + (x - 1)
        new_player, new_opponent = apply_move(player_bb, opponent_bb, 1 << i)
        score = -negamax(new_opponent, new_player, depth - 1, -beta, -alpha)
        if score > best_score:
            best_score, best_move = score, [x, y]
        alpha = max(alpha, best_score)
    return best_move


# 対戦相手のモデルをここで選択
opponent = cpu_lv5.cpu_lv5

if __name__ == "__main__":
    app = ReversiGUI(first_algorithm=cpu_algorithm, second_algorithm=opponent)
    app.gui.mainloop()
