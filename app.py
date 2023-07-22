
import streamlit as st
import pandas as pd
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key
appset_nomal = st.secrets.AppSettings.chatbot_setting
appset_dog = st.secrets.AppSettings.chatbot_setting_dog
appset_cat = st.secrets.AppSettings.chatbot_setting_cat
appset_rabbit = st.secrets.AppSettings.chatbot_setting_rabbit
appset_elephant = st.secrets.AppSettings.chatbot_setting_elephant


# モデルのコールバック関数
def update_appset(selcted_animal):
    if selcted_animal == "汎用":
        appset = appset_nomal
    elif selcted_animal == "犬":
        appset = appset_dog
    elif selcted_animal == "猫":
        appset = appset_cat
    elif selcted_animal == "兎":
        appset = appset_rabbit
    elif selcted_animal == "象":
        appset = appset_elephant
    else:
        appset = appset_nomal

    st.session_state["messages"] = [
    {"role": "system", "content": appset}
    ]

    st.title("AI Assistant"+speaker)

    
# ---------- サイドバー ----------
st.sidebar.title("st.sidebar")

# ---------- temperatureの設定 ----------
y = st.sidebar.slider(label='temperature', min_value=0.0, max_value=2.0, value=0.7)
st.sidebar.write("値が高いほどランダム性が増します")

# ----------　モデルの選択　----------
df_side = pd.DataFrame({
    "animal": ["汎用", "犬", "猫", "兎", "象"],
    "color": ["赤", "青", "黄", "白", "黒"]
    })
selected_side = st.sidebar.selectbox(
    "どの設定を選びますか？",
    df_side["animal"],
    key='selcted_animal'
    )
st.sidebar.write("あなたは" + str(selected_side) + "を選びました！")

# ----------　モデルの決定　----------
st.sidebar.button('決定', on_click=update_appset, args=(st.session_state['selcted_animal'],))




# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": appset_nomal}
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
        if message["role"]=="assistant" and str(selected_side) == "犬":
            speaker="🐶"
        elif message["role"]=="assistant" and str(selected_side) == "猫":
            speaker="😺"
        elif message["role"]=="assistant" and str(selected_side) == "兎":
            speaker="🐰"
        elif message["role"]=="assistant" and str(selected_side) == "象":
            speaker="🐘"
        elif message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])


