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

    for items in data["prompts"]:
        if not isinstance(items , dict):
            raise ValueError("each saved prompt must be in dict .")

        if "text" not in prompts[items] or "id" not in prompts[items]:
            raise ValueError("Id or Text is not available in prompts")

        if type(item["id"]) is not int:
            raise ValueError("Prompt id muse be an integer.")

        if items["id"] <= 0:
            raise ValueError("Id should be postive")

        if not isinstance( items["Text"] , str ):
            raise ValueError("Text should be in string")

        if not item["text"].strip():
            raise ValueError("Prompt text cannot be empty ")

    for items in data["responses"]:
        if not isinstance(items , dict):
            raise ValueError("responses should be dictionary")

        

        if "id" not in responses[items] or "prompt_id" not in responses[items] or "response" not in responses[items]:
            raise ValueError("Id or prompt_id or response is missing")

        if items["id"] <= 0 or items["prompt_id"] <= 0 :
            raise ValueError("Prompt_id or Response_id is incorrect ")

        if type(items["responses"]) is not str:
            raise ValueError("response should be string")


        


    return data

