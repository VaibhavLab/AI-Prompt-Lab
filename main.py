import json

prompt = {} # dict of prompt with number 
prompts = [] # List of the promptss , prompt 


class prompt:
    def __init__(self, prompt_id , text, response ):
        




def mock_response(prompt_text):
    return f"Mock answer for: {prompt_text}"


def give_response(prompt_text):
    return mock_response(prompt_text)
    

def save_data(prompts):
    data = {
        "prompts" : prompts,
        }
    
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_data():# Load data ------------------------------>
    try:
        with open("data.json" , "r" , encoding = "utf-8") as file :
            data = json.load(file)
    except FileNotFoundError:
        return {"prompts" : []}

    return data

data = load_data()
prompts = data["prompts"]


while True:
    print("\nAI Prompt Lab")
    print("1. Add prompt")
    print("2. View prompts")
    
    print("3. Get prompt response ")
    print("4. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        prompt_text = input("Enter your prompt: ").strip()

        if prompt_text:
            prompt = {
                "id" : len(prompts) + 1,
                "text": prompt_text , 
                "Response" : give_response(prompt_text)
            }
            
            prompts.append(prompt)
            print("Your response : " , prompt["Response"])
            print("Prompt added.")
        else:
            print("Prompt cannot be empty.")

    elif choice == "2":
        if prompts:
            for prompt in prompts:
                print(f"{prompt['id']}. {prompt['text']} Response :  {prompt["Response"]}")
        else:
            print("No prompts yet.")
        
    elif choice == "3":
        entered_prompt = input("Enter your prompt : ").strip()
        found = False

        for pro in prompts :
            if pro["text"] == entered_prompt:
                print(f" Your response : {pro["Response"]}")
                found = True
                break

        if not found:
            print("Enter the correct prompt")
        

    elif choice == "4":
        save_data(prompts)
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Please enter 1, 2, 3 or 4.")