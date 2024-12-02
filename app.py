## --------------------------- IMPORT LIBRARIES ---------------------------
import streamlit as st
import random
import google.generativeai as gen_ai
import os

## --------------------------- HELPER FUNCTIONS ---------------------------
def set_subject(topic):
    """
    Sets the subject string based on the selected topic.
    """
    if topic == "Technology":
        st.session_state.subject_string = "Act like a technology expert and help me with this conversation."
    elif topic == "Marketing":
        st.session_state.subject_string = "Act like a marketing expert and help me with this conversation."
    elif topic == "Fitness":
        st.session_state.subject_string = "Act like a fitness expert and help me with this conversation."
    else:  # No topic selected
        st.session_state.subject_string = ""

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

## --------------------------- STREAMLIT PAGE CONFIGURATION ---------------------------
st.set_page_config(
    page_title="Chat-Pilot",
    page_icon="assets/bot-face.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

## --------------------------- INITIALIZE GEMINI CLIENT ---------------------------
# Set your Google Gemini API key
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

## --------------------------- SESSION STATE INITIALIZATION ---------------------------
if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-pro"

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "subject_string" not in st.session_state:
    st.session_state.subject_string = ""

## --------------------------- PAGE HEADER ---------------------------
st.header('Chat-Pilot', divider="green")

## --------------------------- TOPIC SELECTION ---------------------------
# Create topic selector using st.pills
topic_map = {
    "Technology": ":material/computer:",
    "Marketing": ":material/monitoring:",
    "Fitness": ":material/exercise:",
}

# Get user selection
selection = st.pills(
    label="Choose a topic (optional)",
    options=topic_map.keys(),
    selection_mode="single",
    format_func=lambda topic: topic_map.get(topic, "") + "  " + topic if topic else "None",
    key="chatTopic",
    label_visibility="collapsed"
)

# Update subject state based on the selected pill
set_subject(selection)

## --------------------------- DISPLAY CHAT HISTORY ---------------------------
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

## --------------------------- ERROR MESSAGES ---------------------------
error_messages = [
    "**Oops! Looks like we've hit the API usage limit.**\nPlease try again later or check your plan.",
    "**It seems the API is temporarily unavailable due to quota limits.**\nCome back soon!",
    "**API limit exceeded!**\nUpgrade your plan or retry after some time.",
    "**The API quota has been reached.**\nTry again later or adjust your usage limits."
]

## --------------------------- USER INPUT & GEMINI API INTERACTION ---------------------------
user_prompt = st.chat_input("Ask Gemini-Pro...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Prepare the prompt by appending the subject string if it exists
    full_prompt = st.session_state.subject_string + "\n" + user_prompt if st.session_state.subject_string else user_prompt

    # Display spinner while waiting for Gemini's response
    with st.spinner("thinking..."):
        try:
            # Send user's message to Gemini and get the response
            gemini_response = st.session_state.chat_session.send_message(full_prompt)

            # Display Gemini-Pro's response
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)

        except Exception as e:
            # Handle any other exceptions and display the error message
            error_message = f"**An error occurred:** {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_message)



## --------------------------- SIDEBAR ABOUT SECTION ---------------------------
with st.sidebar:
    with st.expander("About", icon=":material/self_improvement:"):
        st.write(
            """
            **Welcome to Chat-Pilot!**\n
            Your smart chat companion, designed to deliver personalized conversations with prompt retention for context-aware interactions. 🚀\n
            Stay tuned for future updates
            """
        )

    # Add footer at the bottom
    st.markdown(
        """
        <div style="position: fixed; bottom:0; text-align: center; font-size: 0.7em; padding: 2px 0;">
            Chat-Pilot can make mistakes. Check important info.
        </div>
        """,
        unsafe_allow_html=True
    )
