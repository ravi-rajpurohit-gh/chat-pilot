## Import libraries
import openai
from openai import OpenAI
import streamlit as st
import random

# def load_css():
#     with open("static/styles.css", "r") as f:
#         css = f"<style>{f.read()}</style>"
#         st.markdown(css, unsafe_allow_html=True)

def set_topic(topic):
    st.session_state.topic = topic

def set_subject():
    if st.session_state.subject_code == 0:
        st.session_state.subject_string = ""
    elif st.session_state.subject_code == 1:
        st.session_state.subject_string = "Act like a technology expert and help me with this conversation."
    elif st.session_state.subject_code == 2:
        st.session_state.subject_string = "Act like a marketing expert and help me with this conversation."
    elif st.session_state.subject_code == 3:
        st.session_state.subject_string = "Act like a fitness expert and help me with this conversation."

## Set page configuration
st.set_page_config(
    page_title="Chat-Pilot",
    page_icon="assets/bot-face.png",
    layout="centered"
)

## Load/Create session variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "topic" not in st.session_state:
    st.session_state.topic = None

if "subject_string" not in st.session_state:
    st.session_state["subject_string"] = ""

if "subject_code" not in st.session_state:
    st.session_state["subject_code"] = 0

## Page Title
st.header('Chat-Pilot', divider="green")




# ## create a topic selector -
topic_map = {
    "Technology": ":material/computer:",
    "Marketing": ":material/monitoring:",
    "Fitness": ":material/exercise:",
}

selection = st.pills(
    label="Choose a topic (optional)",
    options=topic_map.keys(),
    selection_mode="single",
    format_func=lambda topic: topic_map[topic] + "  " + topic,
    key="chat-topic"
)






# Creating three columns for horizontal button alignment
col1, col2, col3 = st.columns(3)

# Adding buttons to each column
with col1:
    if st.button("Technology", icon=":material/computer:", use_container_width=True):
        st.session_state.subject_code = 0 if st.session_state.subject_code == 1 else 1
        set_subject()
        # st.write("You selected Technology", st.session_state.subject_code)

with col2:
    if st.button("Marketing", icon=":material/monitoring:", use_container_width=True):
        st.session_state.subject_code = 0 if st.session_state.subject_code == 2 else 2
        set_subject()
        # st.write("You selected Marketing", st.session_state.subject_code)

with col3:
    if st.button("Fitness", icon=":material/exercise:", use_container_width=True):
        st.session_state.subject_code = 0 if st.session_state.subject_code == 3 else 3
        set_subject()
        # st.write("You selected Fitness", st.session_state.subject_code)


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

## Initialize OpenAI client
# Replace with your actual API key or fetch it from a secure location
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

## Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Predefined error messages
error_messages = [
    "**Oops! Looks like we've hit the API usage limit.**\nPlease try again later or check your plan.",
    "**It seems the API is temporarily unavailable due to quota limits.**\nCome back soon!",
    "**API limit exceeded!**\nUpgrade your plan or retry after some time.",
    "**The API quota has been reached.**\nTry again later or adjust your usage limits."
]


# User input and API interaction
if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("thinking..."):
        try:
            # OpenAI API call
            stream = client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[].extend([
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ]),
                    stream=True,
                )

            with st.chat_message("assistant"):
                stream = stream
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except openai.RateLimitError:
            # Define a user-friendly error message
            error_message = random.choice(error_messages)
            # Display the error message in the chat
            with st.chat_message("assistant"):
                st.markdown(error_message)
            # Save the error message as part of the chat history
            st.session_state.messages.append({"role": "assistant", "content": error_message})

