from models import RunResult
import time 

def Time_Taken(func):
    def wrapper(*args , **kwargs):
        start = time.perf_counter()

        result = func(*args , **kwargs)

        end = time.perf_counter()

        print(end - start)

        return result

    return wrapper 

class PromptRunner:
    def __init__(self, provider):
        self.provider = provider
    @Time_Taken   
    def run(self , prompt , run_id):
        response_text = self.provider.generate(prompt.text)

        return RunResult(
            prompt_id = prompt.id,
            run_id = run_id,
            response = response_text
        )