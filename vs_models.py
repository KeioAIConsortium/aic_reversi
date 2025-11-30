from src.ReversiGUI import ReversiGUI
from cpu import cpu_lv0, cpu_lv1, cpu_lv2, cpu_lv3, cpu_lv4, cpu_lv5
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


def cpu_algorithm(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(board, player_num, x,
                                              y):  # その(x,y)座標に石を置けるか判定
                valid_moves.append([x, y])  # 置けるマスとしてリストに追加
    if valid_moves != []:  # 置けるマスがある場合
        return valid_moves[0]
    return valid_moves


# 相手のモデルをここで選択
opponent = cpu_lv0.cpu_lv0  # ランダム
# opponent = cpu_lv1.cpu_lv1  # 最も多くの石をひっくり返せる手を選ぶ
# opponent = cpu_lv2.cpu_lv2  # コーナー優先戦略
# opponent = cpu_lv3.cpu_lv3  # 位置の重み付けに基づいて手を選ぶ
# opponent = cpu_lv4.cpu_lv4  # 以前の授業での最強モデル
# opponent = cpu_lv5.cpu_lv5  # αβ法で最善手を選ぶモデル

if __name__ == "__main__":
    app = ReversiGUI(first_algorithm=cpu_algorithm, second_algorithm=opponent)
    app.gui.mainloop()
