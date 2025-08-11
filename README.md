# aic_reversi

##  1. 環境構築
### uvのインストール
```sh
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 実行環境の起動
```sh
uv venv --python 3.11
source .venv/bin/activate
```
- Pythonのversionがtkinterに対応していることを確認してください．対応していない場合は画面が表示されません．

## 2. Reversiアプリの起動
```sh
python main.py
```

## 3. アルゴリズムの実装
`main.py`を開き，`cpu_algorism`関数を編集してください．
```python
def cpu_algorism(board, player_num):
    valid_moves = []  # 置けるマスかを格納するリスト
    for x in range(1, 9):  # 1行ずつ走査
        for y in range(1, 9):  # 1列ずつ走査
            if ReversiGUI.validate_reversible(
                board, player_num, x, y
            ):  # その(x,y)座標に石を置けるか判定
                valid_moves.append((x, y))  # 置けるマスとしてリストに追加
    if valid_moves != []:  # 置けるマスがある場合
        return valid_moves[0]
    return valid_moves
``` 

## 4. 過去モデルとの対戦
`vs_bestmodel.py`を使用して過去のモデルと対戦できます．
`cpu_algorism`関数に自分のアルゴリズムを実装してください．
対戦相手のモデルは，以下（3行目）を変えることで変更できます．
```python
from spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用
```
### 実行
```sh
python vs_bestmodel.py
```

## 🏆 過去の大会

### 🌸 spring_2025
高校三年生を対象としたPython初級講座．
CPUを実装し対戦ゲームを実施．
👏 **team aが優勝** 👏

### 🍧 aicdays_2025
一貫校の高校生を対象にしたPython初級講座．
モジュール化されたコードを用いてCPUを実装．
👏 **team XXXが優勝** 👏