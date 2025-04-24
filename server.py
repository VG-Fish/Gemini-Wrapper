from flask import Flask
from environs import env
from google import genai

app: Flask = Flask(__name__)
app.debug = False

env.read_env()
gemini_api_key: str = env.str("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)

# response = client.models.generate_content(
#     model="gemini-2.0-flash-001", contents=
# )
# print(response.text)
