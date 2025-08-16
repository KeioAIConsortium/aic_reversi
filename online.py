from src.Online import Online


def on_put(board, player_num, x, y):
    pass


def polling(player_num):
    pass


def on_init():
    pass


if __name__ == "__main__":
    online = Online(
        on_put=on_put,
        polling=polling,
        on_init=on_init,
        online_first=True,
        local_algorithm=None,
    )
    online.gui.mainloop()
