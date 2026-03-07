# from models.spring_2025.best_algorithm import cpu_move_pred_2 as cpu_algorithm
from models.spring_2026.best_algorithm import cpu_algorithm


# 以前の授業での最強モデル
def cpu_lv4(board, player_num):
    return cpu_algorithm(board, player_num)
