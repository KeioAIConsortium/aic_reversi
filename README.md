# aic_reversi

## 環境構築
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

## Reversiアプリの起動
```sh
python main.py
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