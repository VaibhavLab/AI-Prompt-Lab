import json
from models import Prompt, RunResult 
from Providers import BaseProvider , MockProvider , UppercaseMockProvider , GeminiProvider , OpenRouter
from runner import PromptRunner
from storage import load_data , save_data
import logging 

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Model loaded")

prompts = [] # The list of all the prompts which is in dict 
# ---------------But but but now this is storing object after the little change 
responses = [] # the list of respnses which is also in dict 


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


def run_prompt(runner):
    try:
        prompt_id = int(input("Enter prompt ID: ").strip())
    except ValueError:
        print("Prompt ID must be a number.")
        return

    prompt = find_prompt_by_id(prompt_id)

    if prompt is None:
        print("Prompt not found.")
        return

    response = runner.run(prompt, run_id=len(responses) + 1)

    responses.append(response)

    print("Response:")
    print(response.response)


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

def main():
    global prompts
    global responses

    try:
        data = load_data()
    except ValueError as e:
        print(e)
        return

    provider = OpenRouter()  
    runner = PromptRunner(provider)

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
            save_data(prompts, responses)

        elif choice == "2":
            view_prompts()

        elif choice == "3":
            run_prompt(runner)
            save_data(prompts, responses)

        elif choice == "4":
            view_history()

        elif choice == "5":
            save_data(prompts, responses)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, 4 or 5.")

if __name__ == "__main__":
    main()
