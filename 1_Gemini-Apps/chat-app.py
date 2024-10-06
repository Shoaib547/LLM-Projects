# import libraries
from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# load environment variables
load_dotenv()

# configure api key
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# initialize the model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# function to get the response
def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# initialize streamlit app
st.set_page_config(page_title='Gemini Chat App')
st.header("Chat App 😎")

# initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# take input from the user
input = st.text_input("Input ⬇️", key="input")
submit = st.button("submit ▶️")

if submit and input:
    st.success("Text submitted successfully!")
    st.subheader("🤖...")

    response = get_gemini_response(input)

    # add user input and response to chat history
    st.session_state['chat_history'].append(('You 👨🏻', input))

    full_res = ""
    for chunk in response:
        full_res += chunk.text
    st.write(full_res)
    st.session_state['chat_history'].append(('Bot 🤖', full_res))

st.markdown("---")
st.subheader("Chat History:")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

st.markdown("---")
st.markdown("Created by Shoaib")
