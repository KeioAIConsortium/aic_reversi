from src.ReversiGUI import ReversiGUI, Algorithm_type


class Online(ReversiGUI):
    def __init__(
        self,
        on_put: callable,  # 置いたときのコールバック
        polling: callable,  # 定期的に呼び出されるコールバック
        on_init: callable,  # 初期化時のコールバック
        online_first: bool = False,  # オンラインが先手の場合はTrue、後手の場合はFalse):
        local_algorithm: Algorithm_type = None,  # PC上で動かすアルゴリズム，デフォルトは手動
    ):
        if online_first:
            super().__init__(first_algorithm=None, second_algorithm=local_algorithm)
        else:
            super().__init__(first_algorithm=local_algorithm, second_algorithm=None)

        self.on_put = on_put
        self.polling = polling
        self.on_init = on_init
        self.online_first = online_first

        if online_first:
            self.on_init()

    def online_turn(self):
        if (self.player_num == 1 and self.online_first) or (
            self.player_num == -1 and not self.online_first
        ):
            result, board, player_num = self.polling(player_num=self.player_num)
            if not result:
                self.gui.after(1000, self.online_turn)

            self.board = board
            self.update_board()
            if self.check_game_end():
                return
            self.gui.after(100, self.check_cpu_move)

        if player_num == self.player_num or self.validate_reversible_all(
            self.board, self.player_num
        ):
            self.show_message(
                "パス",
                f"{'●' if self.player_num == 1 else '○'}は置ける場所がありません。パスします。",
            )
            self.player_num = self.rival_player_num(self.player_num)
            self.online_turn()

    # override
    def check_cpu_move(self):
        if (self.player_num == 1 and self.online_first) or (
            self.player_num == -1 and not self.online_first
        ):
            self.gui.after(100, self.online_turn)
        elif (self.player_num == 1 and self.first_algorithm is not None) or (
            self.player_num == -1 and self.second_algorithm is not None
        ):
            self.gui.after(100, self.cpu_turn)

    # override
    def cpu_turn(self):
        # CPUの手番である場合の処理
        if (self.player_num == 1 and self.first_algorithm is not None) or (
            self.player_num == -1 and self.second_algorithm is not None
        ):
            if self.player_num == 1:
                move = self.first_algorithm(self.board, self.player_num)
            else:
                move = self.second_algorithm(self.board, self.player_num)

            if move == []:
                self.show_message(
                    "エラー",
                    "置ける場所がない状況でアルゴリズムが呼ばれました",
                )
                return

            x, y = move
            success, netboard, _ = self.on_put(self.board, self.player_num, x, y)
            newboard = self.put_disc(self.board, self.player_num, x, y)
            if not success and netboard != newboard:
                self.show_message("エラー", "ネットワークエラー")
                return

            self.board = newboard
            self.player_num = self.rival_player_num(self.player_num)
            self.pass_count = 0
            self.update_board()
            if self.check_game_end():
                return
            self.gui.after(100, self.check_cpu_move)

        # もし相手が置ける場所がない場合は再帰する
        if not self.validate_reversible_all(self.board, self.player_num):
            self.show_message(
                "パス",
                f"{'●' if self.player_num == 1 else '○'}は置ける場所がありません。パスします。",
            )
            self.player_num = self.rival_player_num(self.player_num)
            self.cpu_turn()

    # override
    def on_click(self, event):
        # CPUの手番中はクリックを無視する
        if (self.player_num == 1 and self.first_algorithm is not None) or (
            self.player_num == -1 and self.second_algorithm is not None
        ):
            return

        x = event.x // 50 + 1
        y = event.y // 50 + 1

        if self.validate_reversible(self.board, self.player_num, x, y):
            success, _ = self.on_put(self.board, self.player_num, x, y)
            if not success:
                self.show_message("エラー", "ネットワークエラー")
                return
            self.board = self.put_disc(self.board, self.player_num, x, y)
            self.player_num = self.rival_player_num(self.player_num)
            self.pass_count = 0
        else:
            self.show_message("無効", "その場所には置けません。")
            return

        if self.check_game_end():
            return

        if not self.validate_reversible_all(self.board, self.player_num):
            self.pass_count += 1
            self.player_num = self.rival_player_num(self.player_num)
            self.show_message(
                "パス",
                f"{'●' if self.player_num == -1 else '○'}は置ける場所がありません。パスします。",
            )

            if self.pass_count == 2:
                self.update_board()
                self.gui.after(100, self.show_result)
                return
        else:
            self.pass_count = 0

        self.update_board()
        self.gui.after(100, self.check_cpu_move)  # 次のCPU手番をチェック
