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

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        return {
            "prompts": [],
            "responses": []
        }

    except json.JSONDecodeError:
        print("data.json is damaged or contains invalid JSON.")

        return {
            "prompts": [],
            "responses": []
        }

    return data