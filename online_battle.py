from src.ReversiGUI import ReversiGUI
from src.online_model import online_model

"""
CPUの手を選択する関数

引数:
- board: 10x10の2次元リスト形式の盤面。
- player_num: 現在のプレイヤーの番号（1または-1）。

動作内容:
- 盤面の内部部分(1,1)～(8,8)の各セルを走査する。
- 各セルについて、ReversiGUI.validate_reversible関数を用いてその場所に石を置けるか判定する。
- 置けるセルが見つかった場合、そのセルの座標 (x, y) を有効な手としてリストに追加する。
- 有効な手が存在する場合は、その中から手を選んで返す。
- 有効な手が存在しない場合は、空のリストを返す。

返り値:
- valid_moves: 有効な手が存在する場合は選択された手（タプル (x, y) ）、そうでなければ空のリストを返す。

過去の優勝モデルと戦う場合：以下を使用

def cpu_algorithm(board, player_num):
    from models.spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用

    return cpu_move(board, player_num)  # 過去の優勝モデルを使用
"""


def cpu_algorithm(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(
                board, player_num, x, y
            ):  # その(x,y)座標に石を置けるか判定
                valid_moves.append([x, y])  # 置けるマスとしてリストに追加
    if valid_moves != []:  # 置けるマスがある場合
        return valid_moves[0]
    return valid_moves


online_model(is_first=True, local_algorithm=cpu_algorithm)
