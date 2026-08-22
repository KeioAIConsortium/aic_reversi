# 以前の授業での最強モデル
def cpu_lv4(board, player_num):
    from models.spring_2026.best_algorithm import cpu_algorithm  # 循環importを避けるため遅延import

    return cpu_algorithm(board, player_num)
