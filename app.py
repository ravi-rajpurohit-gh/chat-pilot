## --------------------------- IMPORT LIBRARIES ---------------------------
import openai
from openai import OpenAI
import streamlit as st
import random

## --------------------------- HELPER FUNCTIONS ---------------------------
def set_subject(topic):
    """
    Sets the subject code and subject string based on the selected topic.
    """
    if topic == "Technology":
        st.session_state.subject_string = "Act like a technology expert and help me with this conversation."
    elif topic == "Marketing":
        st.session_state.subject_string = "Act like a marketing expert and help me with this conversation."
    elif topic == "Fitness":
        st.session_state.subject_string = "Act like a fitness expert and help me with this conversation."
    else:  # No topic selected
        st.session_state.subject_string = ""

## --------------------------- STREAMLIT PAGE CONFIGURATION ---------------------------
st.set_page_config(
    page_title="Chat-Pilot",
    page_icon="assets/bot-face.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

## --------------------------- SESSION STATE INITIALIZATION ---------------------------
if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

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

## --------------------------- INITIALIZE OPENAI CLIENT ---------------------------
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

## --------------------------- DISPLAY CHAT HISTORY ---------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

## --------------------------- ERROR MESSAGES ---------------------------
error_messages = [
    "**Oops! Looks like we've hit the API usage limit.**\nPlease try again later or check your plan.",
    "**It seems the API is temporarily unavailable due to quota limits.**\nCome back soon!",
    "**API limit exceeded!**\nUpgrade your plan or retry after some time.",
    "**The API quota has been reached.**\nTry again later or adjust your usage limits."
]

## --------------------------- USER INPUT & API INTERACTION ---------------------------
if prompt := st.chat_input("Ask me something..."):
    # Append user input to messages
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call OpenAI API and handle responses
    with st.spinner("thinking..."):
        try:
            # Build the prompt with subject customization
            full_prompt = [{"role": "system", "content": st.session_state.subject_string}] if st.session_state.subject_string else []
            full_prompt += [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

            # Make OpenAI API call
            response = ""
            stream = client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=full_prompt,
                stream=True
            )

            # Stream the response
            with st.chat_message("assistant") as message_container:
                for chunk in stream:
                    message_content = chunk["choices"][0].get("delta", {}).get("content", "")
                    response += message_content
                    message_container.markdown(response)
            # Save assistant's message
            st.session_state.messages.append({"role": "assistant", "content": response})
        except openai.RateLimitError:
            # Handle RateLimitError
            error_message = random.choice(error_messages)
            with st.chat_message("assistant"):
                st.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
        except Exception as e:
            # Handle any other exceptions
            error_message = f"**An error occurred:** {str(e)}"
            with st.chat_message("assistant"):
                st.markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})


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





























#### footer

# from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
# from htbuilder.units import percent, px
# from htbuilder.funcs import rgba, rgb


# def image(src_as_string, **style):
#     return img(src=src_as_string, style=styles(**style))


# def link(link, text, **style):
#     return a(_href=link, _target="_blank", style=styles(**style))(text)


# def layout(*args):

#     style = """
#     <style>
#       # MainMenu {visibility: hidden;}
#       footer {visibility: hidden;}
#      .stApp { bottom: 105px; }
#     </style>
#     """

#     style_div = styles(
#         position="fixed",
#         left=0,
#         bottom=0,
#         margin=px(0, 0, 0, 0),
#         width=percent(100),
#         color="black",
#         text_align="center",
#         height="auto",
#         opacity=1
#     )

#     style_hr = styles(
#         display="block",
#         margin=px(8, 8, "auto", "auto"),
#         border_style="inset",
#         border_width=px(2)
#     )

#     body = p()
#     foot = div(
#         style=style_div
#     )(
#         hr(
#             style=style_hr
#         ),
#         body
#     )

#     st.markdown(style, unsafe_allow_html=True)

#     for arg in args:
#         if isinstance(arg, str):
#             body(arg)

#         elif isinstance(arg, HtmlElement):
#             body(arg)

#     st.markdown(str(foot), unsafe_allow_html=True)


# def footer():
#     myargs = [
#         "Made in ",
#         image('https://avatars3.githubusercontent.com/u/45109972?s=400&v=4',
#               width=px(25), height=px(25)),
#         " with ❤️ by ",
#         link("https://twitter.com/ChristianKlose3", "@ChristianKlose3"),
#         br(),
#         link("https://buymeacoffee.com/chrischross", image('https://i.imgur.com/thJhzOO.png')),
#     ]
#     layout(*myargs)


# if __name__ == "__main__":
#     footer()
