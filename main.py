import os
import streamlit as st
from PIL import Image
import pytesseract
from openai import OpenAI

# Set your OpenAI API key securely

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Prescription Check")

# Input: text and/or image
text_input = st.text_input("Summarise your symptoms and Enter exact prescription (with dosage) in detail:")
uploaded_image = st.file_uploader("Optional: upload prescription image (please Crop out any names)", type=["jpg", "jpeg", "png","HEIC","heic"])

if st.button("Submit"):
    # Process image if provided
    prescription = text_input

    if uploaded_image:
        image = Image.open(uploaded_image)
        prescription_scan = pytesseract.image_to_string(image)
    # else:
    #     prescription = text_input

    st.write("Extracted Prescription:")
    st.write(prescription, ":\n", prescription_scan)

    # Prepare prompt for LLM
    prompt = (
        "Prescription:\n"
        f"{prescription}\n\n\n"

        "Prescription reference read from image (unreliable):\n"
        f"{prescription_scan}"
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert mental health practitioner that checks if a prescription for Geriatric mental health makes sense with. make sure to respond succinctly and only about the prescriptions as follows: (1. Report if there is a fault in prescription or any critical issues like medicines on wrong time or too much quantity or incompatible with symptoms if provided. (2. Report if there is an addiction causing medicine or major side effects causing drug. (3. Report if image is unreadable and ask for text input if not clear"},
            {"role": "user", "content": prompt}
        ],
        model="gpt-4o",
    )

    result = chat_completion.choices[0].message.content.strip()

    st.write("Results:")
    st.write(result)



