from huggingface_hub import InferenceClient
import io
import tempfile
import os
import streamlit as st


HF_API_KEY=st.secrets["HFKEY"]

client = InferenceClient(
    model="google/vit-base-patch16-224",
    token=HF_API_KEY
)

def classify_image(image):
    # Save PIL Image to temporary file and pass the path
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        image.save(tmp_file, format="JPEG")
        tmp_path = tmp_file.name
    
    try:
        result = client.image_classification(tmp_path)
    finally:
        os.unlink(tmp_path)  # Clean up temp file
    
    return result

