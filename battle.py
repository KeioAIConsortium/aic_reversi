import questionary
from src.ReversiGUI import ReversiGUI
from model import cpu_algorithm
from models.cpu import cpu_lv0, cpu_lv1, cpu_lv2, cpu_lv3, cpu_lv4, cpu_lv5
from models.spring_2026.best_algorithm import cpu_algorithm as best_algorithm
from models.alphabeta.alphabeta import cpu_algorithm as alphabeta_algorithm

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

# MODELS = {
#     "human": None,  # 人間
#     "lv0": cpu_lv0.cpu_lv0,  # ランダム
#     "lv1": cpu_lv1.cpu_lv1,  # 最も多くの石をひっくり返せる手を選ぶ
#     "lv2": cpu_lv2.cpu_lv2,  # コーナー優先戦略
#     "lv3": cpu_lv3.cpu_lv3,  # 位置の重み付けに基づいて手を選ぶ
#     "lv4": cpu_lv4.cpu_lv4,  # 以前の授業での最強モデル
#     "lv5": cpu_lv5.cpu_lv5,  # αβ法で最善手を選ぶモデル
#     "student_best": best_algorithm,  # 最適なアルゴリズム
#     "alphabeta": alphabeta_algorithm,  # αβ法で最善手を選ぶモデル
# }

MODELS = {
    "human": {
        "algorithm": None,
        "description": "人間",
    },
    "lv0": {
        "algorithm": cpu_lv0.cpu_lv0,
        "description": "ランダム",
    },
    "lv1": {
        "algorithm": cpu_lv1.cpu_lv1,
        "description": "最も多くの石をひっくり返せる手を選ぶ",
    },
    "lv2": {
        "algorithm": cpu_lv2.cpu_lv2,
        "description": "コーナー優先戦略",
    },
    "lv3": {
        "algorithm": cpu_lv3.cpu_lv3,
        "description": "位置の重み付けに基づいて手を選ぶ",
    },
    "lv4": {
        "algorithm": cpu_lv4.cpu_lv4,
        "description": "以前の授業での最強モデル",
    },
    "lv5": {
        "algorithm": cpu_lv5.cpu_lv5,
        "description": "αβ法で最善手を選ぶモデル",
    },
    "student_best": {
        "algorithm": best_algorithm,
        "description": "受講生が作った中で一番強いモデル",
    },
    "alphabeta": {
        "algorithm": alphabeta_algorithm,
        "description": "αβ法で最善手を選ぶモデル",
    },
}

if __name__ == "__main__":
    # model_name = questionary.select(
    #     "使用するモデルを選択してください",
    #     choices=list(MODELS.keys()),
    # ).ask()
    model_name = questionary.select(
        "使用するモデルを選択してください",
        choices=[
            questionary.Choice(title=f"{name} - {info['description']}", value=name)
            for name, info in MODELS.items()
        ],
    ).ask()
    if model_name is None:
        raise SystemExit

    app = ReversiGUI(
        first_algorithm=(cpu_algorithm, "cpu"),
        second_algorithm=(
            MODELS.get(model_name, {"algorithm": cpu_algorithm})["algorithm"],
            model_name,
        ),
    )
    app.gui.mainloop()
