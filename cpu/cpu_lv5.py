from src.ReversiGUI import ReversiGUI
from cpu.util import find_valid_moves
import copy

# αβ探索を使ったオセロの思考エンジン

# 評価関数で使う重み行列（x=1..8, y=1..8 に対応）
WEIGHTS = [
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100],
]


def evaluate(bd, my_player):
    """
    単純な評価関数:
     - 角の占有に高い重み
     - 位置ごとの重み和
     - 石の差
     - 可動度（置ける手の数）の差
    返り値は my_player に対するスコア（大きいほど良い）
    """
    # 石差
    my_count = 0
    opp_count = 0
    pos_score = 0
    for y in range(1, 9):
        for x in range(1, 9):
            cell = bd[y][x]
            if cell == my_player:
                my_count += 1
                pos_score += WEIGHTS[y - 1][x - 1]
            elif cell == -my_player:
                opp_count += 1
                pos_score -= WEIGHTS[y - 1][x - 1]

    disc_diff = my_count - opp_count

    # 角のボーナス（重めに扱う）
    corners = [(1, 1), (1, 8), (8, 1), (8, 8)]
    corner_score = 0
    for (cx, cy) in corners:
        if bd[cy][cx] == my_player:
            corner_score += 25
        elif bd[cy][cx] == -my_player:
            corner_score -= 25

    # 可動度（利き）の差
    my_moves = len(find_valid_moves(bd, my_player))
    opp_moves = len(find_valid_moves(bd, -my_player))
    mobility = my_moves - opp_moves

    # 重み付けして合成
    score = (10 * disc_diff) + (800 * corner_score) + (5 *
                                                       mobility) + pos_score
    return score


# αβ探索本体
def alphabeta(bd, depth, alpha, beta, current_player, player_num):
    # 終端判定: 深さ0または両者パス（置ける手が無い）
    my_moves = find_valid_moves(bd, player_num)
    # ここで current_player が盤面上での手番

    moves = find_valid_moves(bd, current_player)
    if depth == 0 or (not moves and not find_valid_moves(bd, -current_player)):
        return evaluate(bd, player_num)

    if current_player == player_num:
        # maximizing
        value = -10**9
        if not moves:
            # パス: 相手の手番へ移行
            return alphabeta(bd, depth - 1, alpha, beta, -current_player,
                             player_num)
        for (x, y) in moves:
            # 盤面コピーして手を打つ
            new_bd = copy.deepcopy(bd)
            # ReversiGUI.put_disc はボードを直接変更するためコピーを渡す
            ReversiGUI.put_disc(new_bd, current_player, x, y)
            val = alphabeta(new_bd, depth - 1, alpha, beta, -current_player,
                            player_num)
            if val > value:
                value = val
            if value > alpha:
                alpha = value
            if alpha >= beta:
                break
        return value
    else:
        # minimizing
        value = 10**9
        if not moves:
            return alphabeta(bd, depth - 1, alpha, beta, -current_player,
                             player_num)
        for (x, y) in moves:
            new_bd = copy.deepcopy(bd)
            ReversiGUI.put_disc(new_bd, current_player, x, y)
            val = alphabeta(new_bd, depth - 1, alpha, beta, -current_player,
                            player_num)
            if val < value:
                value = val
            if value < beta:
                beta = value
            if alpha >= beta:
                break
        return value


# αβ法で最善手を選ぶモデル
def cpu_lv5(board, player_num, max_depth: int = 4):
    """
	αβ法で最善手を返す

	- board: 10x10 の盤面リスト（ReversiGUI と互換）
	- player_num: 探索対象となるプレイヤー（1 または -1）
	- max_depth: 探索深さの上限（デフォルト4）
	"""

    # 置ける手を取得（util.find_valid_moves を活用）
    valid_moves = find_valid_moves(board, player_num)
    if not valid_moves:
        return []

    # ルートでの最善手探索
    best_score = -10**9
    best_move = valid_moves[0]
    alpha = -10**9
    beta = 10**9
    for (x, y) in valid_moves:
        # それぞれの手を試してスコアを評価（元の board は変更しない）
        new_bd = copy.deepcopy(board)
        ReversiGUI.put_disc(new_bd, player_num, x, y)
        score = alphabeta(new_bd, max_depth - 1, alpha, beta, -player_num,
                          player_num)
        # 詳細ログを残したい場合はここで print しても良い
        if score > best_score:
            best_score = score
            best_move = [x, y]
        if score > alpha:
            alpha = score

    return best_move
