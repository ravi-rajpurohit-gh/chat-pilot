## Import libraries
import openai
from openai import OpenAI
import streamlit as st
import random

## Set page configuration
st.set_page_config(
    page_title="Chat-Pilot",
    page_icon="assets/bot-face.png",
    layout="centered"
)

# # Inject custom CSS for background color
# st.markdown(
#     """
#     <style>
#     body {
#         background-color: #f0f0f0; /* Light gray background */
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

## Page Title
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

## Initialize OpenAI client
# Replace with your actual API key or fetch it from a secure location
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

## Load/Create session variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

## Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Predefined error messages
error_messages = [
    "🚫 **Oops! Looks like we've hit the API usage limit.**\n\nPlease try again later or check your plan.",
    "⚠️ **It seems the API is temporarily unavailable due to quota limits.**\n\nCome back soon!",
    "❗ **API limit exceeded!**\n\nUpgrade your plan or retry after some time.",
    "🔄 **The API quota has been reached.**\n\nTry again later or adjust your usage limits."
]


# User input and API interaction
if prompt := st.chat_input("Ask me something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # OpenAI API call
        stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
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

