import streamlit as st
import requests
import re

def format_list(text: str) -> str:
    text = re.sub(r'(?<=\d)\. ', '.\n', text)  # Numbered lists
    text = re.sub(r'(?<=\n)- ', '\n- ', text)  # Bullets (basic)
    return text


st.set_page_config(page_title="Your AI Medical Assistant", page_icon="🧠")
st.title("🧠 Your AI Medical Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Format full conversation as prompt
    formatted_prompt = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            formatted_prompt += f"### Human: {msg['content']}\n"
        else:
            formatted_prompt += f"### Assistant: {msg['content']}\n"
    formatted_prompt += "### Assistant:"  # cue for the model

    # Display assistant message placeholder
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("_Thinking..._")

    try:
        # Call FastAPI backend
        response = requests.post(
            "http://localhost:8001/prompt_model",
            json={"prompt": formatted_prompt}
        )

        if response.status_code == 200:
            output = response.json().get("response", "").strip()
        else:
            output = f"Error: {response.status_code}"

    except Exception as e:
        output = f"Exception: {e}"
    # Format the output before displaying it
    #output = format_list(output)

    # Display and save assistant message
    msg_placeholder.markdown(output)
    st.session_state.messages.append({"role": "assistant", "content": output})
