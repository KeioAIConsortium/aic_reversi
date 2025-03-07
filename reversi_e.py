import tkinter as tk
from tkinter import messagebox
import copy
import random

"""
盤面を初期化して返す関数

引数:
- なし。

概要:
- リバーシのゲーム用盤面を初期状態にセットアップする。
- 盤面は10x10の2次元リストで表現し、実際のプレイ部分は(1,1)～(8,8)である。
- 盤面の外枠はゲームに使用しないため、値2を設定する。

初期配置:
- 外枠（xまたはyが0または9）のマスには2を設定。
- 中央4マスでは、(4,5)と(5,4)に黒石（1）、(4,4)と(5,5)に白石（-1）を配置する。
- その他の内部セルは空き（0）とする。

返り値:
- board: 初期化された盤面（10x10の2次元リスト）
"""
def initialize_board():
    board = [[0] * 10 for _ in range(10)]
    for y in range(10):
        for x in range(10):
            if x == 0 or y == 0 or x == 9 or y == 9:
                board[y][x] = 2
            elif x == 4 and y == 5 or x == 5 and y == 4:
                board[y][x] = 1
            elif x == 4 and y == 4 or x == 5 and y == 5:
                board[y][x] = -1
    print(board)
    return board

"""
盤面の状態をコンソールに表示する関数

引数:
- board: 10x10の2次元リスト形式の盤面。ゲームで使用する部分は(1,1)～(8,8)に格納される。

動作内容:
- 内部の各マスを走査し、マスの値に応じて以下の記号を出力する。
    * 黒石（1） → "X"
    * 白石（-1） → "O"
    * 空き（0）   → "."
- 各行の表示後に改行して、盤面全体を出力する。

返り値:
- なし。標準出力に盤面の状態を表示する。
"""
def print_board(board):
    for y in range(1, 9):
        for x in range(1, 9):
            if board[y][x] == 1:
                print("X", end=" ")
            elif board[y][x] == -1:
                print("O", end=" ")
            else:
                print(".", end=" ")
        print()


"""
相手プレイヤーの番号を返す関数

引数:
- player_num: 現在のプレイヤーの番号（黒石なら1、白石なら-1）。

動作内容:
- 現在のプレイヤー番号の符号を反転させることで、相手のプレイヤー番号を求める。

返り値:
- 相手プレイヤーの番号（player_numが1なら-1、-1なら1）。
"""
def rival_player_num(player_num):
    return -player_num

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
def count_reverse(board, player_num, x_put, y_put, x_direction, y_direction):
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

"""
指定された場所に石を置けるか確認する関数

引数:
- board: 10x10の2次元リスト形式の盤面。
- player_num: 現在のプレイヤーの番号（1または-1）。
- x, y: 石を置く予定の位置の座標（盤面内部の位置、1～8）。

動作内容:
- 指定位置が盤面内部かつ空き（値が0）であるかをまず確認する。
- その後、8方向（上下左右および斜め）について、count_reverse関数を用い、
ひとつでも相手の石をひっくり返せる方向があれば有効な手と判断する。

返り値:
- 指定位置に石を置ける場合はTrue、置けない場合はFalse。
"""
def validate_reversible(board, player_num, x, y):
    if x < 1 or x > 8 or y < 1 or y > 8 or board[y][x] != 0:
        return False
    if count_reverse(board, player_num, x, y, -1, -1) > 0:
        return True
    if count_reverse(board, player_num, x, y, -1, 0) > 0:
        return True
    if count_reverse(board, player_num, x, y, -1, 1) > 0:
        return True
    if count_reverse(board, player_num, x, y, 0, -1) > 0:
        return True
    if count_reverse(board, player_num, x, y, 0, 1) > 0:
        return True
    if count_reverse(board, player_num, x, y, 1, -1) > 0:
        return True
    if count_reverse(board, player_num, x, y, 1, 0) > 0:
        return True
    if count_reverse(board, player_num, x, y, 1, 1) > 0:
        return True
    return False

"""
盤面全体で置ける場所があるか確認する関数

引数:
- board: 10x10の2次元リスト形式の盤面。
- player_num: 現在のプレイヤーの番号（1または-1）。

動作内容:
- 盤面の内部部分(1,1)～(8,8)の全てのマスを走査し、各マスに対してvalidate_reversible関数を用いて石を置けるか確認する。
- ひとつでも有効な手が存在すれば探索を中断する。

返り値:
- 現在のプレイヤーが盤面上で石を置ける場所が存在すればTrue、存在しなければFalse。
"""
def validate_reversible_all(board, player_num):
    for y in range(1, 9):
        for x in range(1, 9):
            if validate_reversible(board, player_num, x, y):
                return True
    return False

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
def put_disc(board, player_num, x, y):
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
    print(new_board)
    return new_board

"""
各プレイヤーの石の数を数える関数

引数:
- board: 10x10の2次元リスト形式の盤面。

動作内容:
- 盤面の内部部分(1,1)～(8,8)を走査し、黒石（1）と白石（-1）の個数をカウントする。

返り値:
- discs_list: 黒石の数と白石の数をそれぞれリスト形式で返す。[黒石の数, 白石の数]
"""
def count_discs(board):
    black = 0
    white = 0
    for y in range(1, 9):
        for x in range(1, 9):
            if board[y][x] == 1:
                black += 1
            elif board[y][x] == -1:
                white += 1
    discs_list = [black, white]
    return discs_list

"""
CPUの手を選択する関数

引数:
- board: 10x10の2次元リスト形式の盤面。
- player_num: 現在のプレイヤーの番号（1または-1）。

動作内容:
- 盤面の内部部分(1,1)～(8,8)の各セルを走査する。
- 各セルについて、validate_reversible関数を用いてその場所に石を置けるか判定する。
- 置けるセルが見つかった場合、そのセルの座標 (x, y) を有効な手としてリストに追加する。
- 有効な手が存在する場合は、その中から手を選んで返す。
- 有効な手が存在しない場合は、空のリストを返す。

返り値:
- valid_moves: 有効な手が存在する場合は選択された手（タプル (x, y) ）、そうでなければ空のリストを返す。
"""


# 実装例：選べる手のうち最初の手を選ぶ（弱い！）
import random
def cpu_move(board, player_num):

    valid_moves = []
    for x in range(1, 9):
        for y in range(1, 9):
            if validate_reversible(board, player_num, x, y):
                valid_moves.append((x, y))
    if valid_moves == []:
        return valid_moves

    if validate_reversible(board,player_num,1,1):
        return (1,1)
    if validate_reversible(board,player_num,1,8):
        return (1,8)
    if validate_reversible(board,player_num,8,1):
        return (8,1)
    if validate_reversible(board,player_num,8,8):
        return (8,8)

    disc_num = sum(count_discs(board))
    val = [[-1000000000 for x in range(1, 10)] for y in range(1, 10)]

    for x in range(1, 9):
        for y in range(1, 9):
            if validate_reversible(board, player_num, x, y):
                now = 0
                s = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx != 0 or dy != 0:
                            s += count_reverse(board, player_num, x, y, dx, dy)
                if disc_num <= 25:
                    now = -s
                else:
                    now = s

                fn = False
                if disc_num >= 25 and (x, y) in [
                    (3, 1), (6, 1), (3, 2), (6, 2), (1, 3), (2, 3), (3, 3), (6, 3), (7, 3), (8, 3),
                    (1, 6), (2, 6), (3, 6), (6, 6), (7, 6), (8, 6), (3, 7), (6, 7), (3, 8), (6, 8)
                ]:
                    now += 100
                
                if (x, y) in [
                    (2, 1), (7, 1), (1, 2), (2, 2), (7, 2), (8, 2),
                    (1, 7), (2, 7), (7, 7), (8, 7), (2, 8), (7, 8)
                ]:
                    now -= 100
                
                if disc_num <= 30:
                    if x == 1 or x == 8 or y == 1 or y == 8:
                        now -= 5

                val[x][y] = now
                
    tmp = -10000000000
    moves = []
    for x in range(1, 9):
        for y in range(1, 9):
            tmp = max(tmp, val[x][y])
    for x in range(1, 9):
        for y in range(1, 9):
            if val[x][y] == tmp:
                moves.append((x, y))
    random.shuffle(moves)
    return moves[0]


#TODO: 強いCPUをグループで実装しよう！



 
class ReversiGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("リバーシ")
        self.board = initialize_board()
        self.player_num = 1
        self.pass_count = 0
        
        self.cpu_first = False
        self.cpu_second = False

        # CPU設定:
        # 先手をCPUにする場合は以下のコメントアウトを外す
        # self.cpu_first = True
        # 後手をCPUにする場合は以下のコメントアウトを外す
        self.cpu_second = True

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.info_label = tk.Label(self.master, text="現在のプレイヤー: ●")
        self.info_label.pack()
        
        self.update_board()
        self.master.update()

        # CPU先手の場合は、初回に直接CPUの手番を呼び出す
        if self.cpu_first:
            self.master.after(100, self.cpu_turn)
        else:
            self.master.after(100, self.check_cpu_move)

    def check_cpu_move(self):
        if (self.player_num == 1 and self.cpu_first) or (self.player_num == -1 and self.cpu_second):
            self.master.after(100, self.cpu_turn)
    
    def cpu_turn(self):
        # CPUの手番である場合の処理
        if (self.player_num == 1 and self.cpu_first) or (self.player_num == -1 and self.cpu_second):
            # この関数を変更
            move = cpu_move(self.board, self.player_num)
            if move != []:
                x, y = move
                self.board = put_disc(self.board, self.player_num, x, y)
            else:
                messagebox.showinfo("パス", f"{'●' if self.player_num == 1 else '○'}は置ける場所がありません。パスします。")
            self.player_num = rival_player_num(self.player_num)
            self.pass_count = 0
            self.update_board()
            if self.check_game_end():
                return
            # 次の手番がCPUの場合、再度チェック
            self.master.after(100, self.check_cpu_move)
    
    def update_board(self):
        self.canvas.delete("all")
        for y in range(8):
            for x in range(8):
                x0, y0 = x * 50, y * 50
                x1, y1 = x0 + 50, y0 + 50
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")
                cell = self.board[y+1][x+1]
                if cell == 1:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="black")
                elif cell == -1:
                    self.canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="white")

        self.info_label["text"] = f"現在のプレイヤー: {'●' if self.player_num == 1 else '○'}"

    def show_result(self):
        black, white = count_discs(self.board)
        if black > white:
            winner = "●の勝ち"
        elif black < white:
            winner = "○の勝ち"
        else:
            winner = "引き分け"
        messagebox.showinfo("ゲーム終了", f"ゲーム終了！\n黒: {black}, 白: {white}\n{winner}")
        self.master.destroy()

    def check_game_end(self):
        if not validate_reversible_all(self.board, 1) and not validate_reversible_all(self.board, -1):
            self.update_board()
            self.master.after(100, self.show_result)
            return True
        return False

    def on_click(self, event):
        # CPUの手番中はクリックを無視する
        if (self.player_num == 1 and self.cpu_first) or (self.player_num == -1 and self.cpu_second):
            return
        
        x = event.x // 50 + 1
        y = event.y // 50 + 1

        if validate_reversible(self.board, self.player_num, x, y):
            self.board = put_disc(self.board, self.player_num, x, y)
            self.player_num = rival_player_num(self.player_num)
            self.pass_count = 0
        else:
            messagebox.showwarning("無効", "その場所には置けません。")
            return

        if self.check_game_end():
            return

        if not validate_reversible_all(self.board, self.player_num):
            self.pass_count += 1
            self.player_num = rival_player_num(self.player_num)
            messagebox.showinfo("パス", f"{'●' if self.player_num == -1 else '○'}は置ける場所がありません。パスします。")

            if self.pass_count == 2:
                self.update_board()
                self.master.after(100, self.show_result)
                return
        else:
            self.pass_count = 0

        self.update_board()
        self.master.after(100, self.check_cpu_move)  # 次のCPU手番をチェック

if __name__ == "__main__":
    root = tk.Tk()
    app = ReversiGUI(root)
    root.mainloop()
