import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("Model loaded")


text = input("Enter the prompt: ")

OPENROUTER_API_KEY = ""


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


response = generate(text)

print(response)