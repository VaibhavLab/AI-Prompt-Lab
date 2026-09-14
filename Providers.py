from abc import ABC, abstractmethod

class BaseProvider(ABC): # TypeError : generate is abstract
    @abstractmethod
    def generate(self , prompt_text):
        pass 


class MockProvider(BaseProvider):
    def generate(self , prompt_text):
        return f"Mock answer for : {prompt_text}"


class UppercaseMockProvider(BaseProvider):
    def generate(self , prompt_text):
        return f"Mock answer : {prompt_text.upper()}"   