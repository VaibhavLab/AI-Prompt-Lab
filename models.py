from dataclasses import dataclass



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