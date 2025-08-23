from src.Online import Online
import requests
from spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用

URL = "https://script.google.com/macros/s/AKfycbzCrYJLbnkiMHzNscXcbikvbBX7fOsaF-AlDUk180WS7b75hqHA55lQgFAy8Hn9cAdO/exec"


def on_put(player_num, row, col):
    print(player_num, row, col)
    res = requests.post(
        URL, json={"action": "put", "player": player_num, "row": row, "col": col}
    )
    if res.status_code == 200:
        print(res.text)
        data = res.json()
        if data["status"] == "Success":
            return [True, data["board"], data["player"]]
        else:
            print("Error:", data["message"])
            return [False, None, None]


def polling():
    res = requests.get(URL)
    if res.status_code == 200:
        data = res.json()
        print(data)
        return [True, data["board"], data["player"]]

    else:
        print("Network error")
        return [False, None, None]


def on_init():
    res = requests.post(URL, json={"action": "init"})
    if res.status_code == 200:
        print(res.text)
        data = res.json()
        if data["status"] == "Success":
            return True, data["board"], data["player"]
        else:
            print("Error:", data["message"])
            return False, None, None
    else:
        print("Network error")
        return False, None, None


if __name__ == "__main__":
    online = Online(
        on_put=on_put,
        polling=polling,
        on_init=on_init,
        online_first=True,
        local_algorithm=cpu_move,
    )
    online.gui.mainloop()
