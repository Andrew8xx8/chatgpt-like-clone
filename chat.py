from openai import OpenAI
import streamlit as st
import json

st.title("ChatGPT-like clone")

client = OpenAI()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    system_role_json = st.text_area("Enter JSON with system role", '{"role": "system", "content": "You are helpfull assistant"}')
    if st.button("Set System Role"):
        try:
            system_role = json.loads(system_role_json)
            if "role" in system_role and "content" in system_role:
                st.session_state.messages.append(system_role)
                st.success("System role set successfully.")
            else:
                st.error("Invalid JSON format. Please include 'role' and 'content'.")
        except json.JSONDecodeError:
            st.error("Invalid JSON. Please correct it and try again.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

