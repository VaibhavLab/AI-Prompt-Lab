import json
from dataclasses import dataclass

prompts = [] # The list of all the prompts which is in dict 
# ---------------But but but now this is storing object after the little change 
responses = [] # the list of respnses which is also in dict 


def mock_response(prompt_text): # we just created this until have a real API 
    return f"Mock answer for: {prompt_text}"


def add_prompt():
    # obhject of the class prompt 
    
    prompt_text = input("Enter your prompt: ").strip()

    try:
        # Calling class Prompt to add the prompt , we created the object name as "prompt" calling the class Prompt
        prompt = Prompt(prompt_id=len(prompts) + 1, text=prompt_text)
        
    except ValueError as e:
        print(e)
        return

    prompts.append(prompt) # also append that object to the list of objects "prompt"

    print("Prompt added.")


def view_prompts():
    if not prompts:
        print("No prompts yet.")
        return
    
    # viewering prompt from prompts list we have created containg objects 
    # finding each object 
    for prompt in prompts:
        print(f"{prompt.id}. {prompt.text} ({prompt.word_count} words)")


def find_prompt_by_id(prompt_id):
    for prompt in prompts:
        if prompt.id == prompt_id:
            return prompt

    return None


def run_prompt():
    try:
        prompt_id = int(input("Enter prompt ID: ").strip())
    except ValueError:
        print("Prompt ID must be a number.")
        return

    prompt = find_prompt_by_id(prompt_id)

    if prompt is None:
        print("Prompt not found.")
        return

    response_text = mock_response(prompt.text)

    # Calling the RunResult class and createing the object response
    response = RunResult( 
        prompt_id  = prompt.id , 
        run_id = len(responses) + 1 , 
        response = response_text
    )

    responses.append(response)

    print("Response:")
    print(response_text)


def view_history():
    if not responses:
        print("No response history yet.")
        return

    for response in responses:
        prompt = find_prompt_by_id(response.prompt_id)

        if prompt is not None:
            print(
                f"\nRun ID: {response.run_id}"
                f"\nPrompt ID: {prompt.id}"
                f"\nPrompt: {prompt.text}"
                f"\nResponse: {response.response}"
            )
@dataclass # simplty for practise
class RunResult:
    prompt_id: int
    run_id: int
    response: str

    def to_dict(self):
        return{
            "prompt_id" : self.prompt_id,
            "response" : self.response,
            "id" : self.run_id
        }
    @classmethod # to tell the class it is it's method which helps to run __init__ when called 
    # converting dict to class objects 
    def from_dict(cls, data):
        return cls(
            prompt_id = data["prompt_id"],
            run_id = data["id"],
            response = data["response"]
        )
    


class Prompt:
    def __init__(self, prompt_id , text):
        self.id = prompt_id
        # Assignment calls the text setter below, including during initialization.
        self.text = text

    @property
    def text(self):
        # Reading p.text calls this getter; self refers to the object p.
        return self._text

    @text.setter
    def text(self, value):
        # Assigning p.text = "Hello" passes p as self and "Hello" as value.
        # Validate before storing, so a rejected edit preserves the previous text.
        value = value.strip()
        if not value:
            raise ValueError("Prompt cannot be empty")

        # _text is internal storage by convention, not enforced privacy.
        # Using self.text here would call this setter again recursively.
        self._text = value

    def to_dict(self):
        return {
            "id": self.id,
            "text" : self.text
        }
    @classmethod
    def from_dict(cls , data):
        return cls(
            prompt_id = data["id"],
            text = data["text"]
        )
    @property
    def word_count(self):
        return len(self.text.split())

    def __repr__(self):
        return f"{self.id}. {self.text}"

def save_data():
    data = {
        "prompts": [prompt.to_dict() for prompt in prompts],
        "responses": [response.to_dict() for response in responses]
    }

    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_data():
    try:
        with open("data.json", "r", encoding="utf-8") as file:
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

class MockProvider:
    def generate(self , prompt_text):
        return mock_response(prompt_text)
        



def main():
    global prompts
    global responses

    data = load_data()

    prompts = [Prompt.from_dict(item) for item in data["prompts"] ]
    responses = [RunResult.from_dict(item) for item in data["responses"]]

    while True:
        print("\nAI Prompt Lab")
        print("1. Add prompt")
        print("2. View prompts")
        print("3. Run prompt")
        print("4. View response history")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_prompt()
            save_data()

        elif choice == "2":
            view_prompts()

        elif choice == "3":
            run_prompt()
            save_data()

        elif choice == "4":
            view_history()

        elif choice == "5":
            save_data()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()
