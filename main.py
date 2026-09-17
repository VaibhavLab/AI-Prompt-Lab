from models import Prompt, RunResult
from Providers import OpenRouter
from runner import PromptRunner
from storage import load_data, save_data
import logging
import requests
import asyncio


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)
logger.info("Application started")

prompts = []
responses = []


def add_prompt():
    prompt_text = input("Enter your prompt: ").strip()

    try:
        prompt = Prompt(prompt_id=len(prompts) + 1, text=prompt_text)
    except ValueError as e:
        print(e)
        return

    prompts.append(prompt)
    print("Prompt added.")


def view_prompts():
    if not prompts:
        print("No prompts yet.")
        return

    for prompt in prompts:
        print(f"{prompt.id}. {prompt.text} ({prompt.word_count} words)")


def find_prompt_by_id(prompt_id):
    for prompt in prompts:
        if prompt.id == prompt_id:
            return prompt

    return None


def run_prompt(runner):
    """Run one prompt normally (synchronously)."""
    try:
        prompt_id = int(input("Enter prompt ID: ").strip())
    except ValueError:
        print("Prompt ID must be a number.")
        return

    prompt = find_prompt_by_id(prompt_id)

    if prompt is None:
        print("Prompt not found.")
        return

    try:
        response = runner.run(prompt, run_id=len(responses) + 1)
    except requests.exceptions.RequestException:
        logger.error("AI provider request failed")
        print("The AI request failed.")
        return

    responses.append(response)

    print("Response:")
    print(response.response)


async def run_all_prompts(runner):
    """Run all saved prompts concurrently using the existing synchronous runner."""
    if not prompts:
        print("No prompts to run.")
        return

    tasks = []
    starting_run_id = len(responses) + 1

    for index, prompt in enumerate(prompts):
        # runner.run() is synchronous because the providers use requests.
        # asyncio.to_thread() moves that blocking work to a worker thread so
        # several prompt requests can be in progress at the same time.
        task = asyncio.to_thread(
            runner.run,
            prompt,
            starting_run_id + index
        )
        tasks.append(task)

    try:
        # gather() waits for all of the created async tasks together.
        results = await asyncio.gather(*tasks)
    except requests.exceptions.RequestException:
        logger.error("One or more AI provider requests failed")
        print("One or more AI requests failed.")
        return

    responses.extend(results)

    print("\nAll prompts completed:")
    for result in results:
        prompt = find_prompt_by_id(result.prompt_id)
        print(
            f"\nPrompt ID: {result.prompt_id}"
            f"\nPrompt: {prompt.text if prompt else 'Unknown prompt'}"
            f"\nResponse: {result.response}"
        )


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


async def main():
    global prompts
    global responses

    try:
        data = load_data()
    except ValueError as e:
        print(e)
        return

    provider = OpenRouter()
    runner = PromptRunner(provider)

    prompts = [Prompt.from_dict(item) for item in data["prompts"]]
    responses = [RunResult.from_dict(item) for item in data["responses"]]

    while True:
        print("\nAI Prompt Lab")
        print("1. Add prompt")
        print("2. View prompts")
        print("3. Run prompt")
        print("4. View response history")
        print("5. Run all prompts")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_prompt()
            save_data(prompts, responses)

        elif choice == "2":
            view_prompts()

        elif choice == "3":
            # One prompt does not need concurrency, so this stays synchronous.
            run_prompt(runner)
            save_data(prompts, responses)

        elif choice == "4":
            view_history()

        elif choice == "5":
            # This is async, so it must be awaited from inside async main().
            await run_all_prompts(runner)
            save_data(prompts, responses)

        elif choice == "6":
            save_data(prompts, responses)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 1, 2, 3, 4, 5 or 6.")


if __name__ == "__main__":
    # asyncio.run() creates the event loop and starts our async main function.
    asyncio.run(main())
