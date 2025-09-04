import streamlit as st
import requests

# Streamlit Page
st.title("LLM Prompt Interface")

# Input prompt
prompt = st.text_area("Enter your prompt:", height=200)

# Submit button
if st.button("Submit"):
    if prompt.strip():
        with st.spinner("Sending prompt to the model..."):
            try:
                # Send to API
                response = requests.post(
                    "http://localhost:8001/prompt_model",
                    json={"prompt": prompt.strip()}
                )
                if response.status_code == 200:
                    data = response.json()
                    #st.success("Response received:")
                    st.write(data.get("response", "(No response field in API)"))
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
    else:
        st.warning("Prompt cannot be empty.")
