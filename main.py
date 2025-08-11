from src.ReversiGUI import ReversiGUI

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


def cpu_algorism(board, player_num):
    from spring_2025.best_algorism import cpu_move  # TODO この行を消して実装を行う

    return cpu_move(board, player_num)  # TODO この行を消して実装を行う


if __name__ == "__main__":
    app = ReversiGUI(cpu_algorism=cpu_algorism, cpu_first=True)
    app.gui.mainloop()
