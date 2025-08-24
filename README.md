# aic_reversi

##  1. 環境構築
### uvのインストール
```sh
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### プログラムのダウンロード
```
git clone https://github.com/KeioAIConsortium/aic_reversi.git
cd aic_reversi
```

### 実行環境の起動
```sh
# macOS/Linux
uv venv --python 3.11
source .venv/bin/activate

# Windows
uv venv --python 3.11
.venv\Scripts\activate

```

## 2. Reversiアプリの起動
```sh
uv run python main.py
```
- 何も表示されない場合：Pythonのversionがtkinterに対応していることを確認してください．対応していない場合は画面が表示されません．

## 3. アルゴリズムの実装
`main.py`を開き，`cpu_algorithm`関数を編集してください．
```python
def cpu_algorithm(board, player_num):
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
`cpu_algorithm`関数に自分のアルゴリズムを実装してください．
対戦相手のモデルは，以下（3行目）を変えることで変更できます．
```python
from spring_2025.best_algorism import cpu_move  # 過去の優勝モデルを使用
```
### 実行
```sh
uv run python vs_bestmodel.py
```

## 5. オンライン対戦
`online_battle.py`を使用してオンラインで対戦できます．
`cpu_algorithm`関数に自分のアルゴリズムを実装してください．
`is_first`を`True`にすると先手，`False`にすると後手になります．
### 実行
```sh
python online_battle.py
```

## 🏆 過去の大会

### 🌸 spring_2025
高校三年生を対象としたPython初級講座．
CPUを実装し対戦ゲームを実施．
👏 **team aが優勝** 👏

### 🍧 aicdays_2025
- Python初級
  
  一貫校の中高生を対象にしたPython初級講座．モジュール化されたコードを用いてCPUを実装．
- GAS中上級（GAS×Python）
  
  一貫校の中高生を対象にしたGAS中上級講座．GASを使ってreversiを通信対戦可能に実装．
