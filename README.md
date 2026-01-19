# 吉野会長ナレッジボット

ベステラ株式会社 会長 吉野佳秀の講演内容を基にした対話型Webアプリケーションです。

## デプロイ済みアプリ

**Streamlit Cloud**: https://yoshino-chatbot-e4ngqmceung4ecr3cwbrib.streamlit.app/

## ドキュメント

| ドキュメント | 内容 |
|------------|------|
| [運用手順書](docs/OPERATION.md) | 講演データの追加方法、トラブルシューティング |
| [要件・仕様書](docs/SPECIFICATION.md) | システム構成、機能要件、データ仕様 |

---

## ローカル開発

### 必要なもの

1. **Python 3.8以上**
2. **Anthropic APIキー** - [Anthropic Console](https://console.anthropic.com/) で取得

### 起動方法

#### 方法1: バッチファイルで起動（推奨）

1. `start.bat` をダブルクリック
2. 初回は自動的に仮想環境とパッケージがインストールされます
3. ブラウザで `http://localhost:8501` を開く
4. サイドバーにAPIキーを入力

#### 方法2: 手動で起動

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化（Windows）
venv\Scripts\activate

# パッケージをインストール
pip install -r requirements.txt

# アプリを起動
streamlit run app.py
```

### APIキーの設定

#### 方法1: アプリ内で入力
サイドバーの「Anthropic APIキー」欄に入力

#### 方法2: 環境変数で設定（推奨）
```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

---

## ファイル構成

```
yoshino_chatbot/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 必要なパッケージ
├── yoshino_knowledge_base.md   # ナレッジベース
├── start.bat                   # 起動用バッチファイル
├── README.md                   # このファイル
├── .gitignore                  # Git除外設定
├── 文字起こし/                  # 講演文字起こしCSV
│   ├── 20260115_133109_第1回録画.csv
│   ├── 20260115_133303_第2回録画.csv
│   └── 20260115_133628_第3回録画.csv
└── docs/                       # ドキュメント
    ├── OPERATION.md            # 運用手順書
    └── SPECIFICATION.md        # 要件・仕様書
```

---

## 講演データの追加

新しい講演の文字起こしを追加する手順：

1. **CSVファイルを作成**（形式: `YYYYMMDD_HHMMSS_第N回録画.csv`）
2. **`文字起こし/` フォルダにコピー**
3. **GitHubにプッシュ**
   ```bash
   git add .
   git commit -m "第N回講演の文字起こしを追加"
   git push origin main
   ```
4. **自動デプロイ**: Streamlit Cloudが自動的に更新

詳細は [運用手順書](docs/OPERATION.md) を参照してください。

---

## トラブルシューティング

### 「APIキーが設定されていません」と表示される
- サイドバーでAPIキーを入力してください
- または環境変数 `ANTHROPIC_API_KEY` を設定してください

### 「ナレッジベースが見つかりません」と表示される
- `yoshino_knowledge_base.md` が同じフォルダにあることを確認してください

### ポートが使用中と表示される
- 別のポート番号を指定してください：
  ```bash
  streamlit run app.py --server.port 8502
  ```

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-01-19 | Streamlit Cloudにデプロイ、ドキュメント整備 |
| 2026-01-15 | 初版作成 |
