import json
from models import RunResult , Prompt
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent/"data.json"

"""
This builds the location of data.json beside storage.py:
- __file__ → this module’s file location.
- .resolve() → its full absolute path.
- .parent → the folder containing it.
- / "data.json" → joins that folder with the filename.
Then change the file-opening lines in both functions.
"""


def save_data(prompts , responses):
    data = {
        "prompts": [prompt.to_dict() for prompt in prompts],
        "responses": [response.to_dict() for response in responses]
    }
    temp_file = DATA_FILE.with_suffix(".tmp")


    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temp_file.replace(DATA_FILE)

def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        return {
            "prompts": [],
            "responses": []
        }

    except json.JSONDecodeError as e:
        raise ValueError(
            "data.json contains invalid JSON. Loading stopped . "
        )from e
    
    if not isinstance(data , dict):
        raise ValueError("Saved data must be in dictionary")

    if "prompts" not in data or "responses" not in data:
        raise ValueError("Saved data must contain prompts and responses.")

    if not isinstance(data["prompts"] , list):
        raise ValueError("prompts must be list")

    if not isinstance(data["responses"] , list ):
        raise ValueError("reposnses must be list")

    for item in data["prompts"]:
        if not isinstance(item, dict):
            raise ValueError("Each saved prompt must be a dictionary.")

        if "id" not in item or "text" not in item:
            raise ValueError("Prompt must contain id and text.")

        if type(item["id"]) is not int:
            raise ValueError("Prompt id must be an integer.")

        if item["id"] <= 0:
            raise ValueError("Prompt id must be positive.")

        if not isinstance(item["text"], str):
            raise ValueError("Prompt text must be a string.")

        if not item["text"].strip():
            raise ValueError("Prompt text cannot be empty.")

    for item in data["responses"]:
        if not isinstance(item, dict):
            raise ValueError("Each response must be a dictionary.")

        if ("id" not in item or "prompt_id" not in item or "response" not in item):
            raise ValueError("Response must contain id, prompt_id and response.")

        if type(item["id"]) is not int:
            raise ValueError("Response id must be an integer.")

        if type(item["prompt_id"]) is not int:
            raise ValueError("Prompt id must be an integer.")

        if item["id"] <= 0 or item["prompt_id"] <= 0:
            raise ValueError("Response id and prompt id must be positive.")

        if not isinstance(item["response"], str):
            raise ValueError("Response must be a string.")

    return data


