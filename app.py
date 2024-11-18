## import libraries
from openai import OpenAI
import streamlit as st

## set page configuration
st.set_page_config(
    page_title="Chat-Pilot",
    page_icon="assets/bot-face.png",
    layout="centered"
)

st.title('Chat-Pilot')

# Create an about section for new users
with st.expander("About", icon=":material/self_improvement:"):
    st.write(
        """
        Welcome to **Chat-Pilot**! 🚀
        This is a chat application exploring the use of **Streamlit** and **OpenAI API** 
        to create a dynamic and intuitive chat interface. 

        The vision includes personalized interactions and features like saving key prompts for future use. 
        Stay tuned as this project grows and evolves! 💡
        """
    )


## get the openAI chatgpt object
# openai.api_key = OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

## load/create session
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})