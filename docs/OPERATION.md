# 運用手順書

## 概要

本ドキュメントでは、吉野会長ナレッジボットの運用・更新手順を説明します。

---

## 1. 新しい講演データの追加手順

### 1.1 文字起こしデータの準備

1. **動画を文字起こし**
   - 使用ツール例: Whisper、Google Speech-to-Text、手動文字起こし等

2. **CSVファイルを作成**
   - ファイル名の命名規則: `YYYYMMDD_HHMMSS_第N回録画.csv`
   - 例: `20260120_100000_第4回録画.csv`

3. **CSVフォーマット**
   ```csv
   発言者,発言内容,開始時間,終了時間
   吉野会長,発言内容がここに入ります,00:00:00,00:00:30
   ```
   - 必須列: `発言内容`（30文字以上の発言のみ抽出されます）

### 1.2 ナレッジベースの更新（任意）

重要なトピックがある場合は `yoshino_knowledge_base.md` も更新してください：

1. 該当セクションに新しい内容を追記
2. Q&Aセクションに新しい質問を追加
3. 用語集に新しい専門用語を追加

### 1.3 GitHubへのアップロード

#### 方法A: コマンドライン（推奨）

```bash
# 1. プロジェクトディレクトリに移動
cd C:\Users\h.hasebe\ClaudeCode\yoshino_chatbot

# 2. 新しいCSVファイルを文字起こしフォルダにコピー
# （手動でコピーするか、以下のコマンド）
cp /path/to/新しいファイル.csv 文字起こし/

# 3. 変更をステージング
git add .

# 4. コミット
git commit -m "第N回講演の文字起こしを追加"

# 5. プッシュ
git push origin main
```

#### 方法B: GitHub Web UI

1. https://github.com/hhasebe-besterra/yoshino-chatbot にアクセス
2. `文字起こし` フォルダをクリック
3. 「Add file」→「Upload files」
4. CSVファイルをドラッグ＆ドロップ
5. 「Commit changes」をクリック

### 1.4 自動デプロイ

- GitHubにプッシュすると、Streamlit Cloudが自動的に再デプロイします
- 通常1〜2分でアプリに反映されます
- デプロイ状況: https://share.streamlit.io/ で確認可能

---

## 2. トラブルシューティング

### アプリが動作しない場合

1. **Streamlit Cloud のログを確認**
   - https://share.streamlit.io/ にアクセス
   - アプリを選択 → 「Manage app」→「Logs」

2. **よくあるエラー**
   | エラー | 原因 | 対処法 |
   |--------|------|--------|
   | APIキーエラー | Secretsが未設定または無効 | Streamlit Cloud のSecretsを確認 |
   | ファイルが見つからない | パスの問題 | ファイル名・パスを確認 |
   | CSVエンコーディングエラー | 文字コードの問題 | UTF-8 (BOM付き)で保存し直す |

### APIキーの更新

1. https://share.streamlit.io/ にアクセス
2. アプリを選択 → 「Settings」→「Secrets」
3. `ANTHROPIC_API_KEY` を更新
4. 「Save」→ アプリが自動再起動

---

## 3. バックアップ

### 推奨バックアップ対象

- `yoshino_knowledge_base.md`（ナレッジベース本体）
- `文字起こし/` フォルダ内のCSVファイル

### バックアップ方法

```bash
# GitHubからクローン（別の場所にバックアップ）
git clone https://github.com/hhasebe-besterra/yoshino-chatbot.git backup_yoshino_chatbot
```

---

## 4. 連絡先・サポート

- **GitHub リポジトリ**: https://github.com/hhasebe-besterra/yoshino-chatbot
- **Streamlit Cloud**: https://share.streamlit.io/

---

## 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-01-19 | 初版作成 |
