import streamlit as st
import requests
import re

def format_list(text: str) -> str:
    text = re.sub(r'(?<=\d)\. ', '.\n', text)  # Numbered lists
    text = re.sub(r'(?<=\n)- ', '\n- ', text)  # Bullets (basic)
    return text

API_URI = st.secrets.get("aws_api_uri", "local_api_uri")

st.set_page_config(page_title="Your AI Medical Assistant", page_icon="🧠")
st.title("🧠 Your AI Medical Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": """Hello! How can I help you today?
    If you are feeling unwell, please describe your symptoms.
    I can also assist you with health advice."""}
    ]
if "session_id" not in st.session_state:
    # Generate a unique session ID per user
    st.session_state.session_id = "user_session_1"  # or generate dynamically

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

    # Display assistant message placeholder
    with st.chat_message("assistant"):
        msg_placeholder = st.empty()
        msg_placeholder.markdown("_Thinking..._")

    try:
        # Call FastAPI backend
        response = requests.post(
            f"{API_URI}/prompt_model",
            json={
                "prompt": prompt,  # only send the latest user input
                "session_id": st.session_state.session_id
            }
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
