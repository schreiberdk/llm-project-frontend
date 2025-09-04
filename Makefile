streamlit: streamlit_local

streamlit_local:
	-@API_URI=local_api_uri streamlit run Chatbot.py

streamlit_cloud:
	-@API_URI=aws_api_uri streamlit run Chatbot.py
