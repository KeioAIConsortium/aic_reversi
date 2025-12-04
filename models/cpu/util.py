from src.ReversiGUI import ReversiGUI


def find_valid_moves(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(board, player_num, x,
                                              y):  # その(x,y)座標に石を置けるか判定
                valid_moves.append([x, y])  # 置けるマスとしてリストに追加
    return valid_moves
