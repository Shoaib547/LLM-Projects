from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai 
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# load the model and get the response
def get_gemini_response(input_prompt, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_prompt, image[0], prompt])
    return response.text

# create input prompt
input_prompt = """
You are an invoice extractor. An invoice image will be provided to you, and you have to 
answer the questions asked about this invoice. The invoice can be in any language,
you should be able to answer the questions even if the invoice data is in other languages.
"""

# initialize streamlit app
st.set_page_config(page_title="Multi-language Invoice Reader using Gemini")
st.header("Multi-language Invoice Reader using Gemini")

input = st.text_input("Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Image uplaoded", use_column_width=True)
    st.success("File uplaoded successfully.")

# create image data
def get_image_data(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        return FileNotFoundError("File not uplaoded.")

submit = st.button("Ask the question")

if submit:
    image_data = get_image_data(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is...")
    st.write(response)