# QnA App

# import libraries
from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# load environment variables
load_dotenv()

# configure api key
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# initialize the model
model = genai.GenerativeModel("gemini-pro")

# function to get the response
def get_gemini_response(question):
    response = model.generate_content(question)
    return response.text

# initialize streamlit app
st.set_page_config(page_title='Q&A App')

st.header("Gemini LLM Q&A App")

# take input from the user
input = st.text_input("Input: ", key="input")

# submit button
submit = st.button("Ask this question")

# get the response when submit is clicked
if submit:
    response = get_gemini_response(input)
    st.subheader('The response is...')
    st.write(response)
