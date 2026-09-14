from models import RunResult

class PromptRunner:
    def __init__(self, provider):
        self.provider = provider

    def run(self , prompt , run_id):
        response_text = self.provider.generate(prompt.text)

        return RunResult(
            prompt_id = prompt.id,
            run_id = run_id,
            response = response_text
        )