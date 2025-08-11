from ReversiGUI import ReversiGUI
import random
from typing import Tuple, Literal

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
"""


def cpu_algorism(
    board: list[list[int]],
    player_num: Literal[1, -1],
) -> Tuple[int, int]:

    pri1 = [(1, 1), (1, 8), (8, 1), (8, 8)]
    random.shuffle(pri1)

    pri2 = [
        (1, 3),
        (1, 6),
        (3, 1),
        (3, 3),
        (3, 6),
        (3, 8),
        (6, 1),
        (6, 3),
        (6, 6),
        (6, 8),
        (8, 3),
        (8, 6),
    ]
    random.shuffle(pri2)

    pri3 = [(1, 4), (1, 5), (4, 1), (4, 8), (5, 1), (5, 8), (8, 4), (8, 5)]
    random.shuffle(pri3)

    pri4 = [(2, 3), (2, 5), (3, 2), (3, 7), (5, 2), (5, 7), (6, 3), (6, 6)]
    random.shuffle(pri4)

    pri5 = [
        (2, 4),
        (2, 5),
        (3, 4),
        (3, 5),
        (4, 2),
        (4, 3),
        (4, 6),
        (4, 7),
        (5, 2),
        (5, 3),
        (5, 6),
        (5, 7),
        (6, 4),
        (6, 5),
        (7, 4),
        (7, 5),
    ]
    random.shuffle(pri5)

    dame = [
        (1, 2),
        (1, 7),
        (2, 1),
        (2, 2),
        (2, 7),
        (2, 8),
        (7, 1),
        (7, 2),
        (7, 7),
        (7, 8),
        (8, 2),
        (8, 7),
    ]
    random.shuffle(dame)

    valid_moves = []
    for x in range(1, 9):
        for y in range(1, 9):
            if ReversiGUI.validate_reversible(board, player_num, x, y):
                valid_moves.append((x, y))
    if valid_moves != []:
        print(valid_moves)
        for valid_move in valid_moves:
            for list1 in pri1:
                if valid_move == list1:
                    return valid_move
        for valid_move in valid_moves:
            for list2 in pri2:
                if valid_move == list2:
                    return valid_move
        for valid_move in valid_moves:
            for list3 in pri3:
                if valid_move == list3:
                    return valid_move
        for valid_move in valid_moves:
            for list4 in pri4:
                if valid_move == list4:
                    return valid_move
        for valid_move in valid_moves:
            for list5 in pri5:
                if valid_move == list5:
                    return valid_move

        for valid_move in valid_moves:
            for damene in dame:
                if valid_move != damene:
                    return valid_move

        random.shuffle(valid_moves)
        return valid_moves[0]
    return valid_moves


if __name__ == "__main__":
    demo_board: list[list[int]] = [
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 1, -1, 0, 0, 0, 0, 2],
        [2, 0, 0, -1, 1, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ]
    player_num: int = 1  # プレイヤー1の手番

    next_move = cpu_algorism(demo_board, player_num)
    print("CPUの選択した手:", next_move)
    demo_board[next_move[0]][next_move[1]] = player_num  # CPUの手を盤面に反映
    print("選択後の盤面:")
    for row in demo_board:
        print(row)
