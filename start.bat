@echo off
echo ========================================
echo 吉野会長ナレッジボット 起動中...
echo ========================================
echo.

REM 仮想環境が存在するか確認
if not exist "venv" (
    echo 仮想環境を作成しています...
    python -m venv venv
    call venv\Scripts\activate
    echo 必要なパッケージをインストールしています...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

echo.
echo ブラウザで http://localhost:8501 を開いてください
echo 終了するには Ctrl+C を押してください
echo.
streamlit run app.py --server.port 8501
