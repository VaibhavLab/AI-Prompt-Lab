from abc import ABC, abstractmethod
from dotenv import load_dotenv
import os
import requests 
import logging 

logger = logging.getLogger(__name__)

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


class GeminiProvider(BaseProvider):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            logger.error("Gemini API key is missing")
            raise ValueError("Gemini API is not available")


    def generate(self , prompt_text):
        url = (
            "https://generativelanguage.googleapis.com/"
            "v1beta/models/gemini-3.8-flash:generateContent"
        )

        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt_text
                        }
                    ]
                }
            ]
        }
        try:
            response = requests.post( url , headers = headers , json = payload , timeout = 30 )

            response.raise_for_status()
            data = response.json()

        except requests.exceptions.Timeout:
            logger.error("Gemini request timed out")
            raise

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to Gemini API")
            raise

        except requests.exceptions.HTTPError as e:
            logger.error(f"Gemini API returned an HTTP error: {e}")
            raise

        except requests.exceptions.RequestException as e:
            logger.error(f"Gemini request failed: {e}")
            raise


        return data["candidates"][0]["content"]["parts"][0]["text"]


class OpenRouter(BaseProvider):
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        if not self.api_key:
            logger.error("OPENROUTER API key is missing")
            raise ValueError("OPENROUTER API is not available")

        def generate(prompt_text):

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }

            payload = {
                "model": "openrouter/free",

                "messages": [
                    {
                        "role": "user",
                        "content": prompt_text
                    }
                ]
            }

            try:

                response = requests.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )

                response.raise_for_status()

                data = response.json()

            except requests.exceptions.Timeout:
                logger.error("OpenRouter request timed out")
                raise

            except requests.exceptions.ConnectionError:
                logger.error("Could not connect to OpenRouter API")
                raise

            except requests.exceptions.HTTPError as e:
                logger.error(f"OpenRouter API returned an HTTP error: {e}")
                raise

            except requests.exceptions.RequestException as e:
                logger.error(f"OpenRouter request failed: {e}")
                raise


            return data["choices"][0]["message"]["content"]



        
"""
URL      = delivery address
headers  = labels/instructions on the parcel
payload  = what's inside the parcel
timeout  = how long you're willing to wait for delivery
response = what comes back
"""
""" Must remember 
URL
headers
payload/body
POST request
timeout
check status
parse JSON
extract result
"""