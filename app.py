"""
ベステラ会長 吉野佳秀 ナレッジボット
Streamlit Webアプリケーション
"""

import streamlit as st
import anthropic
import os
import csv
from pathlib import Path

# APIキーを読み込む（優先順位: Streamlit Secrets > 環境変数 > config.env）
def load_api_key():
    """APIキーを読み込む"""
    # 1. Streamlit Secrets（Streamlit Cloud用）
    try:
        if hasattr(st, 'secrets') and 'ANTHROPIC_API_KEY' in st.secrets:
            return st.secrets['ANTHROPIC_API_KEY']
    except Exception:
        pass

    # 2. 環境変数
    if os.environ.get("ANTHROPIC_API_KEY"):
        return os.environ.get("ANTHROPIC_API_KEY")

    # 3. config.envファイル（ローカル開発用）
    config_path = Path(__file__).parent / "config.env"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("set ANTHROPIC_API_KEY="):
                    return line.replace("set ANTHROPIC_API_KEY=", "")
    return None

# 設定されたAPIキー
CONFIGURED_API_KEY = load_api_key()

# 文字起こしCSVファイルを読み込む（要約版：トークン制限対策）
def load_transcriptions():
    """文字起こしフォルダからCSVファイルを読み込む（重要な発言のみ抽出）"""
    transcription_dir = Path(__file__).parent / "文字起こし"
    transcriptions = []

    if transcription_dir.exists():
        for csv_file in sorted(transcription_dir.glob("*.csv")):
            try:
                # ファイル名から回数を抽出
                filename = csv_file.stem
                if "第1回" in filename:
                    session_name = "第1回講演"
                elif "第2回" in filename:
                    session_name = "第2回講演"
                elif "第3回" in filename:
                    session_name = "第3回講演"
                else:
                    session_name = filename

                utterances = []
                with open(csv_file, "r", encoding="utf-8-sig") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        content = row.get("発言内容", "").strip()
                        # 30文字以上の発言のみ抽出（重要な内容のみ）
                        if content and len(content) > 30:
                            utterances.append(content)

                if utterances:
                    # 最大30発言に制限（トークン数削減・レートリミット対策）
                    limited_utterances = utterances[:30]
                    full_text = "\n".join(limited_utterances)
                    transcriptions.append(f"\n### {session_name}の主要な内容\n\n{full_text}")
            except Exception as e:
                continue

    return "\n".join(transcriptions) if transcriptions else ""

# ページ設定
st.set_page_config(
    page_title="吉野会長ナレッジボット",
    page_icon="🏭",
    layout="wide"
)

# カスタムCSS - ベステラコーポレートカラー（赤）
st.markdown("""
<style>
    /* サイドバーの幅を広くする */
    [data-testid="stSidebar"] {
        min-width: 400px;
        max-width: 450px;
    }
    [data-testid="stSidebar"] > div:first-child {
        width: 400px;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #C41E3A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #FFEBEE;
    }
    .assistant-message {
        background-color: #F5F5F5;
    }
    .sidebar-info {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    /* サイドバーのスタイル */
    [data-testid="stSidebar"] {
        background-color: #FFF5F5;
    }
    /* ボタンのスタイル */
    .stButton > button {
        background-color: #C41E3A;
        color: white;
        border: none;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: #A01830;
        color: white;
    }
    /* 成功メッセージの色 */
    .stSuccess {
        background-color: #FFEBEE;
        color: #C41E3A;
    }
    /* リンクの色 */
    a {
        color: #C41E3A;
    }
</style>
""", unsafe_allow_html=True)

# ナレッジベースの読み込み
@st.cache_data
def load_knowledge_base():
    """ナレッジベースファイルと文字起こしを読み込む"""
    knowledge_content = None

    # メインのナレッジベースファイルを読み込み
    kb_path = Path(__file__).parent.parent / "yoshino_knowledge_base.md"
    if kb_path.exists():
        with open(kb_path, "r", encoding="utf-8") as f:
            knowledge_content = f.read()
    else:
        # 同じディレクトリも確認
        kb_path_alt = Path(__file__).parent / "yoshino_knowledge_base.md"
        if kb_path_alt.exists():
            with open(kb_path_alt, "r", encoding="utf-8") as f:
                knowledge_content = f.read()

    if knowledge_content is None:
        return None

    # 文字起こしを追加
    transcriptions = load_transcriptions()
    if transcriptions:
        knowledge_content += "\n\n---\n\n## 講演の文字起こし（追加資料）\n\n以下は講演の文字起こしです。より詳細な会長の発言を参照できます。\n" + transcriptions

    return knowledge_content

# システムプロンプト
def get_system_prompt(knowledge_base: str) -> str:
    return f"""あなたは「ベステラ株式会社 会長 吉野佳秀のナレッジを伝える案内役」です。

## あなたの役割
新入社員や中途採用者からの質問に対して、以下のナレッジベースの内容を基に回答してください。

## 回答のスタイル
1. 会長の言葉を引用: 可能な限り、会長の実際の発言や考えを引用してください
2. 実体験ベース: 抽象論ではなく、会長の実体験に基づいた回答を心がけてください
3. 専門知識の解説: 金属や解体に関する専門用語は、わかりやすく解説してください
4. 教訓の共有: 失敗談から学んだ教訓も積極的に伝えてください
5. 親しみやすさ: 堅苦しくなりすぎず、会長の人柄が伝わるような回答を心がけてください

## 注意事項
- ナレッジベースに記載されていない情報については、「この講演では触れられていませんでした」と正直に伝えてください
- 会長の見解は個人的な意見であることを必要に応じて明示してください

## ナレッジベース
{knowledge_base}
"""

def main():
    # ヘッダー
    st.markdown('<p class="main-header">🏭 吉野会長ナレッジボット</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">ベステラ株式会社 会長 吉野佳秀の50年以上の経験と知識を学ぶ</p>', unsafe_allow_html=True)

    # サイドバー
    with st.sidebar:
        st.image("https://www.besterra.co.jp/images2022/common/logo.svg", width=200)
        st.markdown("### プラント解体のリーディングカンパニー")
        st.markdown("*壊すことを、美しく。*")

        st.markdown("---")

        st.markdown("### 📚 質問できるトピック")
        st.markdown("""
        - 吉野会長の生い立ちと経歴
        - ベステラ創業の経緯
        - 金属に関する専門知識
        - 変圧器の解体と銅の見分け方
        - プラント解体の技術と経験
        - 富士フイルムとコニカの品質管理
        - 出光興産での解体工事
        - 見積もりの考え方と極意
        - 会長の人生哲学と教訓
        """)

        st.markdown("---")

        st.markdown("### 💡 質問の例")
        example_questions = [
            "会長の生い立ちについて教えてください",
            "ベステラ創業のきっかけは何ですか？",
            "富士フイルムとコニカの品質管理の違いは？",
            "硝酸銀を捨てた失敗談について教えてください",
            "出光興産での解体工事のエピソードは？",
            "見積もりで大切なことは何ですか？",
            "姫路城と煙突の高さの話を教えてください",
            "スズメバチとの共存エピソードは？",
        ]
        for q in example_questions:
            if st.button(q, key=f"example_{q[:10]}"):
                st.session_state.example_question = q

        # APIキー設定（CONFIGURED_API_KEYがあれば入力欄を完全に非表示）
        if CONFIGURED_API_KEY:
            # config.envまたは環境変数にAPIキーが設定されている場合
            api_key = CONFIGURED_API_KEY
            # 設定セクション自体を非表示にする（何も表示しない）
        else:
            # APIキーがない場合は入力欄を表示
            st.markdown("---")
            st.markdown("### ⚙️ 設定")
            api_key = st.text_input(
                "Anthropic APIキー",
                type="password",
                help="Claude APIを使用するためのAPIキーを入力してください"
            )
            if api_key:
                st.success("APIキーが設定されています")
            else:
                st.warning("APIキーを入力してください")

    # ナレッジベース読み込み
    knowledge_base = load_knowledge_base()

    if knowledge_base is None:
        st.error("ナレッジベースファイル（yoshino_knowledge_base.md）が見つかりません。")
        st.info("yoshino_knowledge_base.md をこのアプリと同じディレクトリまたは親ディレクトリに配置してください。")
        return

    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 回答待ちフラグの初期化
    if "needs_response" not in st.session_state:
        st.session_state.needs_response = False

    # サンプル質問がクリックされた場合
    if "example_question" in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.needs_response = True
        st.rerun()

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ユーザー入力
    if prompt := st.chat_input("質問を入力してください..."):
        # ユーザーメッセージを追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.needs_response = True

    # 回答生成（新規入力またはサンプル質問クリック時）
    if st.session_state.needs_response:
        st.session_state.needs_response = False

        # APIキーチェック
        if not api_key:
            with st.chat_message("assistant"):
                st.error("APIキーが設定されていません。管理者に連絡してください。")
            return

        # Claude APIで回答生成
        with st.chat_message("assistant"):
            with st.spinner("回答を生成中..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)

                    # メッセージ履歴を構築
                    messages = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]

                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2048,
                        system=get_system_prompt(knowledge_base),
                        messages=messages
                    )

                    assistant_message = response.content[0].text
                    st.markdown(assistant_message)

                    # アシスタントメッセージを履歴に追加
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_message
                    })

                except anthropic.APIError as e:
                    st.error(f"APIエラーが発生しました: {str(e)}")
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

    # 初回表示時のウェルカムメッセージ
    if len(st.session_state.messages) == 0:
        st.markdown("""
        ### 👋 ようこそ！

        このチャットボットでは、ベステラ会長 吉野佳秀の講演内容を基に、
        金属の専門知識やプラント解体の技術、会長の経験談などについて質問できます。

        **左のサイドバー**から質問の例を選ぶか、下の入力欄に直接質問を入力してください。

        ---

        #### 🎯 おすすめの質問
        - 「会長の生い立ちについて教えてください」
        - 「ステンレスの価格はどうやって決まりますか？」
        - 「ベステラを創業したきっかけは何ですか？」
        """)

if __name__ == "__main__":
    main()
