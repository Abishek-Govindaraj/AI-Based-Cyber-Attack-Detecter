import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_chatbot_response(user_message):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=user_message
    )
    return response.text