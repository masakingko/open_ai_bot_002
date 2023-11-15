
import streamlit as st
import pandas as pd
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
# 各種プロンプト設定の取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
appset_nomal = st.secrets.AppSettings.chatbot_setting
appset_dog = st.secrets.AppSettings.chatbot_setting_dog
appset_cat = st.secrets.AppSettings.chatbot_setting_cat
appset_rabbit = st.secrets.AppSettings.chatbot_setting_rabbit
appset_elephant = st.secrets.AppSettings.chatbot_setting_elephant

# モデル（プロンプト）のコールバック関数
def update_appset(selcted_animal):
    if selcted_animal == "犬":
        appset = appset_dog
        speaker_role = "🐶"
    elif selcted_animal == "猫":
        appset = appset_cat
        speaker_role = "😺"
    elif selcted_animal == "兎":
        appset = appset_rabbit
        speaker_role = "🐰"
    elif selcted_animal == "象":
        appset = appset_elephant
        speaker_role = "🐘"
    else:
        appset = appset_nomal
        speaker_role = "🤖"

    st.session_state["messages"] = [
    {"role": "system", "content": appset}
    ]
    st.session_state.role = speaker_role

    
# ---------- サイドバー ----------
st.sidebar.title("設定")
st.sidebar.write("")

# ----------　モデルの選択　----------
df_side = pd.DataFrame({
    "animal": ["汎用", "犬", "猫", "兎", "象"],
    "color": ["赤", "青", "黄", "白", "黒"]
    })
selected_side = st.sidebar.selectbox(
    "誰と話がしたいですか？",
    df_side["animal"],
    key='selcted_animal'
    )
# ----------　モデルの決定　----------
st.sidebar.button('決定', on_click=update_appset, args=(st.session_state['selcted_animal'],))
st.sidebar.write("")
st.sidebar.write("")


# ---------- temperatureの設定 ----------
y = st.sidebar.slider(label='temperature（値が高いほどランダム性が増します）', min_value=0.0, max_value=2.0, value=0.7)


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": appset_nomal}
        ]
    st.session_state.role = "🤖"


# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=y,
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)
    
    st.session_state["user_input"] = ""  # 入力欄を消去


# ---　ユーザーインターフェイスの構築　---
st.title("AI Assistant　　" + str(st.session_state.role))
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker = str(st.session_state.role)

        st.write(speaker + ": " + message["content"])


