# 吉野会長ナレッジボット

ベステラ株式会社 会長 吉野佳秀の講演内容を基にした対話型Webアプリケーションです。

## 必要なもの

1. **Python 3.8以上**
2. **Anthropic APIキー** - [Anthropic Console](https://console.anthropic.com/) で取得

## 起動方法

### 方法1: バッチファイルで起動（推奨）

1. `start.bat` をダブルクリック
2. 初回は自動的に仮想環境とパッケージがインストールされます
3. ブラウザで `http://localhost:8501` を開く
4. サイドバーにAPIキーを入力

### 方法2: 手動で起動

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

## APIキーの設定

### 方法1: アプリ内で入力
サイドバーの「Anthropic APIキー」欄に入力

### 方法2: 環境変数で設定（推奨）
```bash
# Windows
set ANTHROPIC_API_KEY=your-api-key-here

# PowerShell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

## 社内ネットワークで共有する場合

他のPCからアクセスできるようにするには：

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

その後、他のPCから `http://[サーバーのIPアドレス]:8501` でアクセス

## ファイル構成

```
yoshino_chatbot/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 必要なパッケージ
├── yoshino_knowledge_base.md   # ナレッジベース
├── start.bat                   # 起動用バッチファイル
└── README.md                   # このファイル
```

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

## ナレッジベースの更新

第2回以降の講演内容を追加する場合は、`yoshino_knowledge_base.md` を編集してください。
アプリを再起動すると、新しい内容が反映されます。
