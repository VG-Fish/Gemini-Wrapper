from typing import Literal, Dict

from flask import Flask, Response, request, jsonify

from environs import env

from google import genai
from google.genai.errors import APIError
from google.genai.types import FunctionCallingConfig, GenerateContentConfig, GenerateContentResponse, ToolConfig

from werkzeug.exceptions import BadRequest

from errors import InvalidJSON

app: Flask = Flask(__name__)
app.debug = False

env.read_env()
gemini_api_key: str = env.str("GEMINI_API_KEY")
client: genai.Client = genai.Client(api_key=gemini_api_key)

tool_config: ToolConfig = ToolConfig(
    function_calling_config=FunctionCallingConfig(
        mode="NONE"
    )
)
config: GenerateContentConfig = GenerateContentConfig(
    tool_config=tool_config
)

@app.route("/")
def index() -> Literal["Flask app is running."]:
    return "Flask app is running."


@app.route("/gemini", methods=["POST"])
def get_gemini_response() -> Response:
    try:
        data: Dict[str, str] = request.get_json(force=True)
        if "prompt" not in data:
            raise InvalidJSON

        response: GenerateContentResponse = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=data["prompt"],
            config=config
        )

        return jsonify({"output": response.text})
    except BadRequest:
        return jsonify(
            {
                "error": "Either set the current 'Content-Type' header or don't pass in malformed json."
            }
        )
    except APIError:
        return jsonify({"error": "Could not get Google Gemini's response."})
    except InvalidJSON:
        return jsonify(
            {
                "error": "To call Google Gemini, pass in a JSON object with a key of 'prompt' and the value as your prompt."
            }
        )
    except Exception as e:
        return jsonify({"error": f"Unknown error occurred: {e}"})


if __name__ == "__main__":
    app.run()
