import json
from openai import OpenAI
import streamlit as st
from st_bridge import bridge, html
from gpts import GPTs
from menu_html import generate_html_content


def initialize_openai_client():
    return OpenAI()


def setup_streamlit_sidebar(html_content):
    with st.sidebar:
        html(html_content)
        initial_messages_json = st.text_area(
            "Enter JSON with initial messages",
            '[{"role": "system", "content": "You are helpfull assistant"}]',
        )
        if st.button("Set Initial Messages"):
            try:
                initial_messages = json.loads(initial_messages_json)
                if all(
                    "role" in message
                    and message["role"] in ["user", "assistant", "system"]
                    for message in initial_messages
                ):
                    st.session_state.current_messages = initial_messages
                    st.success("Initial messages set successfully.")
                else:
                    st.error(
                        "Invalid JSON format. Please include 'role' and 'content'."
                    )
            except json.JSONDecodeError:
                st.error("Invalid JSON. Please correct it and try again.")


def handle_display_messages():
    for message in st.session_state.current_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(client):
    if prompt := st.chat_input("What is up?"):
        st.session_state.current_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        name = st.session_state.gpt["name"]
        image = st.session_state.gpt["image"]
        with st.chat_message(name, avatar=image):
            message_placeholder = st.empty()
            full_response = ""
            responses = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.current_messages
                ],
                stream=True,
            )

            # pylint: disable=not-an-iterable
            for response in responses:
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.current_messages.append(
            {"role": "assistant", "content": full_response}
        )


st.title("ChatGPT-like clone")
gpt_id = bridge("current-gpt", default=GPTs[0]["id"])
gpt = next((g for g in GPTs if g["id"] == gpt_id), None)
st.session_state.gpt = gpt
st.session_state.current_messages = gpt["inital_messages"]


client = initialize_openai_client()
html_content = generate_html_content(GPTs)
setup_streamlit_sidebar(html_content)
handle_display_messages()
handle_user_input(client)
