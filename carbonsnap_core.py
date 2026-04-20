from groq import Groq
from image_classification import classify_image
import streamlit as st


GROQ_API_KEY=st.secrets["GROQKEY"]



client = Groq(api_key=GROQ_API_KEY)

def model(image):
    output = classify_image(image)
    object = output[0].label

    prompt = f"""
    Analyze the environmental impact of: "{object}"

    Return JSON only:
    {{
    "object": "",
    "category": "",
    "impact_level": "low | medium | high",
    "carbon_estimate": "",
    "explanation": "",
    "alternatives": [],
    "future_impact": "",
    "message":""
    }}

    Keep explanation under 2 lines. Be realistic. Also tell an alarming fact that can happen in the future due to the continous use of the {object} to warn the user.Also add a message to the world 
    """

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ],
        temperature=0.3
    
    )


    res=completion.choices[0].message.content
    return res
