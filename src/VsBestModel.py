from src.ReversiGUI import ReversiGUI


class VsBestModel(ReversiGUI):
    def __init__(
        self,
        cpu_algorism: callable = None,
        cpu_first: bool = False,  # CPUが先手の場合はTrue、後手の場合はFalse):
        best_model: callable = None,  # 過去の優勝モデルを使用する場合は指定する
    ):
        super().__init__(cpu_algorism=cpu_algorism, cpu_first=cpu_first)

        self.canvas.unbind("<Button-1>")  # onclickのbindを削除
        self.best_model = best_model  # 過去の優勝モデルを使用する場合は指定する

    def check_best_model_move(self):
        if (self.player_num == -1 and self.cpu_first) or (
            self.player_num == 1 and not self.cpu_first
        ):
            self.gui.after(100, self.best_model_turn)

    def best_model_turn(self):
        # best model CPUの手番である場合の処理
        if (self.player_num == -1 and self.cpu_first) or (
            self.player_num == 1 and not self.cpu_first
        ):
            move = self.best_model(self.board, self.player_num)
            if move != []:
                x, y = move
                self.board = self.put_disc(self.board, self.player_num, x, y)
            else:
                self.show_message(
                    "パス",
                    f"{'●' if self.player_num == 1 else '○'}は置ける場所がありません。パスします。",
                )
            self.player_num = self.rival_player_num(self.player_num)
            self.pass_count = 0
            self.update_board()
            if self.check_game_end():
                return
            self.gui.after(100, self.check_best_model_move)

        # もしユーザが置ける場所がない場合は再帰する
        if not self.validate_reversible_all(self.board, self.player_num):
            self.show_message(
                "パス",
                f"{'●' if self.player_num == 1 else '○'}は置ける場所がありません。パスします。",
            )
            self.player_num = self.rival_player_num(self.player_num)
            self.best_model_turn()

        self.gui.after(100, self.check_cpu_move)  # 次のCPU手番をチェック

    def cpu_turn(self):
        super().cpu_turn()
        self.gui.after(100, self.check_best_model_move)

    def show_result(self):
        black, white = self.count_discs()
        if self.cpu_first:
            cpu_discs = black
            best_model_discs = white
        else:
            cpu_discs = white
            best_model_discs = black

        if cpu_discs > best_model_discs:
            winner = "CPUの勝ち"
        elif cpu_discs < best_model_discs:
            winner = "BestModelの勝ち"
        else:
            winner = "引き分け"
        self.show_message(
            "ゲーム終了",
            f"ゲーム終了！\nCPU: {cpu_discs}, BestModel: {best_model_discs}\n{winner}",
        )
        self.gui.destroy()
