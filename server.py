from typing import Literal
from flask import Flask, request, jsonify
from environs import env
from google import genai
from google.genai.types import GenerateContentResponse

app: Flask = Flask(__name__)
# app.debug = False

env.read_env()
gemini_api_key: str = env.str("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key)


@app.route("/")
def index() -> Literal["Flask app is running."]:
    return "Flask app is running."


@app.route("/gemini", methods=["POST"])
def get_gemini_response():
    data = request.get_json()

    response: GenerateContentResponse = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=data["content"]
    )

    return jsonify({"output": response.text})


if __name__ == "__main__":
    app.run()
