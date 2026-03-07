from src.ReversiGUI import ReversiGUI
from models.cpu import cpu_lv0, cpu_lv1, cpu_lv2, cpu_lv3, cpu_lv4, cpu_lv5
import copy

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


def rival_player_num(player_num):
    """相手プレイヤーの番号を返す関数"""
    return -player_num


def count_reverse(board, player_num, x_put, y_put, x_direction, y_direction):
    """
    特定方向にひっくり返せる石の数を数える関数

    引数:
    - board: 10x10の2次元リスト形式の盤面。
    - player_num: 現在のプレイヤーの番号（1または-1）。
    - x_put, y_put: 石を置く位置の座標（盤面内部の位置、1～8）。
    - x_direction, y_direction: 石を置いた後に探索する方向を示す単位ベクトル（例：(-1, 0)は左方向、(1, 1)は右下方向）

    動作内容:
    - 指定位置(x_put, y_put)から、指定方向に一マスずつ進みながら探索する。
    - 最初に連続して相手の石（-player_num）がある場合、その数をカウントする。
    - 連続した相手石の先に自分の石（player_num）があれば、そのカウント数がひっくり返せる石の数となる。
    - 途中で盤外（値が2）または自分の石以外の状態になった場合は0を返す。

    返り値:
    - count: 指定方向でひっくり返せる石の数（整数）。条件を満たさない場合は0。
    """
    count = 0
    x = x_put + x_direction
    y = y_put + y_direction
    while board[y][x] == rival_player_num(player_num):
        count += 1
        x += x_direction
        y += y_direction
        if board[y][x] == 2:
            return 0
    if board[y][x] != player_num:
        return 0
    return count


def put_disc(board, player_num, x, y):
    """
    石を置いて盤面を更新する関数

    引数:
    - board: 10x10の2次元リスト形式の盤面。
    - player_num: 現在のプレイヤーの番号（1または-1）。
    - x, y: 石を置く位置の座標（盤面内部の位置、1～8）。

    動作内容:
    - 渡された盤面のコピーを作成し、変更対象とする。
    - 8方向すべてについて、count_reverse関数を用いてひっくり返せる相手の石の数を取得する。
    - 取得したカウントに基づき、各方向に沿って相手の石を現在のプレイヤーの石に置き換える。
    - 最終的に、指定位置に現在のプレイヤーの石を配置する。

    返り値:
    - new_board: 更新された盤面（10x10の2次元リスト）。
    """
    new_board = copy.deepcopy(board)
    for i in range(1, count_reverse(new_board, player_num, x, y, 1, 0) + 1):
        new_board[y][x + i] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, 1, 1) + 1):
        new_board[y + i][x + i] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, 0, 1) + 1):
        new_board[y + i][x] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, -1, 1) + 1):
        new_board[y + i][x - i] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, -1, 0) + 1):
        new_board[y][x - i] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, -1, -1) + 1):
        new_board[y - i][x - i] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, 0, -1) + 1):
        new_board[y - i][x] = player_num
    for i in range(1, count_reverse(new_board, player_num, x, y, 1, -1) + 1):
        new_board[y - i][x + i] = player_num
    new_board[y][x] = player_num
    return new_board


def cpu_algorithm(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for cordinate in [[1, 1], [1, 8], [8, 1], [8, 8]]:  # 1マスずつ走査
        if ReversiGUI.validate_reversible(
            board, player_num, cordinate[0], cordinate[1]
        ):  # その(x,y)座標に石を置けるか判定
            valid_moves.append(cordinate)  # 置けるマスとしてリストに追加


    for cordinate in [[1, 3], [1, 6],[3, 1], [3, 8], [6, 1], [6, 8]]:  # 1マスずつ走査
        if ReversiGUI.validate_reversible(
            board, player_num, cordinate[0], cordinate[1]
            if put_disc(board, rival_player_num(player_num), cordinate[0], cordinate[1]) != None else (cordinate[0], cordinate[1])
        ):  # その(x,y)座標に石を置けるか判定
            valid_moves.append(cordinate)  # 置けるマスとしてリストに追加        

    for cordinate in [[3, 3], [3, 6],[6, 3], [6, 6]]:  # 1マスずつ走査
        if ReversiGUI.validate_reversible(
            board, player_num, cordinate[0], cordinate[1]
            if put_disc(board, rival_player_num(player_num), cordinate[0], cordinate[1]) != None else (cordinate[0], cordinate[1])
        ):  # その(x,y)座標に石を置けるか判定
            valid_moves.append(cordinate)  # 置けるマスとしてリストに追加

    if 
   

    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if (x <= 2 or x >= 7) and (y <= 2 or y >= 7):
                continue
            if ReversiGUI.validate_reversible(
                board, player_num, x, y
            ):  # その(x,y)座標に石を置けるか判定
                valid_moves.append([x, y])  # 置けるマスとしてリストに追加

    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(
                board, player_num, x, y
            ):  # その(x,y)座標に石を置けるか判定
                valid_moves.append([x, y])  # 置けるマスとしてリストに追加

    if valid_moves != []:  # 置けるマスがある場合
        return valid_moves[0]
    return valid_moves


# 相手のモデルをここで選択
# opponent = cpu_lv0.cpu_lv0  # ランダム
# opponent = cpu_lv1.cpu_lv1  # 最も多くの石をひっくり返せる手を選ぶ
# opponent = cpu_lv2.cpu_lv2  # コーナー優先戦略
#opponent = cpu_lv3.cpu_lv3  # 位置の重み付けに基づいて手を選ぶ
#opponent = cpu_lv4.cpu_lv4  # 以前の授業での最強モデル
opponent = cpu_lv5.cpu_lv5  # αβ法で最善手を選ぶモデル

if __name__ == "__main__":
    app = ReversiGUI(first_algorithm=cpu_algorithm, second_algorithm=opponent)
    app.gui.mainloop()
