from src.ReversiGUI import ReversiGUI
from spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用

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

def cpu_algorism(board, player_num):
    from spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用

    return cpu_move(board, player_num)  # 過去の優勝モデルを使用
"""



def cpu_algorism(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(
                board, player_num, x, y
            ):  # その(x,y)座標に石を置けるか判定
                valid_moves.append((x, y))  # 置けるマスとしてリストに追加

    kado_list = [(1,1),(1,8),(8,1),(8,8)]        
    hen_list = [(1,3),(1,4),(1,5),(1,6),(3,1),(4,1),(5,1),(6,1),(3,8),(4,8),(5,8),(6,8),
                (8,3),(8,4),(8,5),(8,6)]
    
    count_1=0
    for y in range (3,6,1):
        if board [y][1]==-1:
            count_1 +=1
        if count_1 == 4:
            hen_list.append ([2,1])
            hen_list.append ([7,1])
    count_2=0
    for x in range (3,6,1):
        if board [1][x]==-1:
            count_2 +=1
        if count_2 == 4:
            hen_list.append ([1,2])
            hen_list.append ([1,7])
    count_3=0
    for y in range (3,6,1):
        if board [y][7]==-1:
            count_3 +=1
        if count_3 == 4:
            hen_list.append ([8,2])
            hen_list.append ([8,7])
    count_4=0
    for x in range (3,6,1):
        if board [7][x]==-1:
            count_4 +=1
        if count_4 == 4:
            hen_list.append ([2,8])
            hen_list.append ([7,8])

    utikado_list = [(3,3),(3,6),(6,3),(6,6)]
    utihen_list = [(4,3),(5,3),(6,4),(6,5),(3,4),(3,5),(4,6),(5,6)]
    utisyuu_list = [(3,2),(4,2),(5,2),(6,2),(7,3),(7,4),(7,5),(7,6),(2,3),(2,4),(2,5),(2,6),(3,7),(4,7),(5,7),(6,7)]
    henkado_list = [(2,1),(7,1),(1,2),(8,2),(1,7),(8,7),(2,8),(7,8)]

    for valid_move in valid_moves:
        for kado in kado_list:
            if valid_move == kado: 
                return valid_move
        for hen in hen_list:
            if valid_move == hen: 
                return valid_move
        for utikado in utikado_list:
            if valid_move == utikado: 
                return valid_move   
        for utihen in utihen_list:
            if valid_move == utihen: 
                return valid_move
        for utisyuu in utisyuu_list:
            if valid_move == utisyuu: 
                return valid_move
        for henkado in henkado_list:
            if valid_move == henkado: 
                return valid_move
    if valid_moves != []:     
            return valid_moves[0]
    return valid_moves
 
if __name__ == "__main__":
    app = ReversiGUI(first_algorithm=cpu_algorism, second_algorithm=cpu_move)
    app.gui.mainloop()
