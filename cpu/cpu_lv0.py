from src.ReversiGUI import ReversiGUI
from cpu.util import find_valid_moves
import random


# ランダムに手を選ぶモデル
def cpu_lv0(board, player_num):
    # 置ける手を探す
    valid_moves = find_valid_moves(board, player_num)
    if valid_moves == []:
        return []

    # ランダムに手を選択して返す
    return random.choice(valid_moves)
