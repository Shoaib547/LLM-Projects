from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai 
import os 
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_prompt, image[0], prompt])
    return response.text

def get_image_parts(uploaded_image):
    if uploaded_image is not None:
        bytes_data = uploaded_image.getvalue()
        image_parts = [{
            "mime_type": uploaded_image.type,
            "data": bytes_data
        }]
        return image_parts
    else:
        return FileNotFoundError("No file detected.")

# input_prompt is the first argument in get_gemini response function
input_prompt = """
You are an expert nutritionist. you need to see the food items from the image
and calculate the total calories, also provide the details of every food items 
with calories intake in below format

Item 1 - No. of calories
Item 2 - No. of calories
-----
-----
"""

# setting up streamlit app
st.set_page_config(page_title="Calories Finder App (Using Gemini)")
st.header("Calories Finder App")

# input is the third argument in get_gemini_response function
input = st.text_input("Input prompt: ", key="prompt")

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# for displaying the image
image = ""
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Get the calories info")

# when submit is clicked
if submit:
    # image data is the second argument in get_gemini_response function
    image_data = get_image_parts(uploaded_image)

    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The response is...")
    st.write(response)