
import streamlit as st
import pandas as pd
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
appset_nomal = st.secrets.AppSettings.chatbot_setting
appset_dog = st.secrets.AppSettings.chatbot_setting_dog
appset_cat = st.secrets.AppSettings.chatbot_setting_cat

a = 0

# モデルのコールバック関数
def update_appset():
    a = 1
    
# ---------- サイドバー ----------
st.sidebar.title("st.sidebar")

# ---------- temperatureの設定 ----------
y = st.sidebar.slider(label='temperature', min_value=0.0, max_value=2.0, value=0.7)
st.sidebar.write("値が高いほどランダム性が増します")

# ----------　モデルの設定　----------
df_side = pd.DataFrame({
    "animal": ["汎用", "犬", "猫", "兎", "象"],
    "color": ["赤", "青", "黄", "白", "黒"]
    })
selected_side = st.sidebar.selectbox(
    "どの設定を選びますか？",
    df_side["animal"],
    on_change=update_appset
    )
st.sidebar.write("あなたは" + str(selected_side) + "を選びました！")

if selected_side == "汎用":
    appset = appset_nomal
elif selected_side == "犬":
    appset = appset_dog
elif selected_side == "猫":
    appset = appset_cat
else:
    appset = appset_nomal


# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state and a==0:
    st.session_state["messages"] = [
        {"role": "system", "content": appset_nomal}
        ]

if "messages" not in st.session_state and a==1:
    st.session_state["messages"] = [
        {"role": "system", "content": appset}
        ]


# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=y
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)
    

    st.session_state["user_input"] = ""  # 入力欄を消去


# ---　ユーザーインターフェイスの構築　---
st.title("AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant" and selected_side == "犬":
            speaker="🐶"
        if message["role"]=="assistant" and selected_side == "猫":
            speaker="😺"
        elif message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])


