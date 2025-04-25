from typing import Self


class InvalidJSON(Exception):
    """This exception will be called when the JSON object that's passed into the '/gemini' webpage
    doesn't contain a key with the name of 'prompt'."""
