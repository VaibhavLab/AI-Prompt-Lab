import json
import time
import pytest
import requests
import storage
from models import Prompt, RunResult
from runner import PromptRunner, Time_Taken

# Ye AI is banvaya hai testing ke liye maine 
# reminidng myself to learn this stuff later 

class SuccessProvider:
    def generate(self, prompt_text):
        return "test response"


class TimeoutProvider:
    def generate(self, prompt_text):
        raise requests.exceptions.Timeout("fake timeout")


class ConnectionFailProvider:
    def generate(self, prompt_text):
        raise requests.exceptions.ConnectionError("fake connection failure")


class HTTPFailProvider:
    def generate(self, prompt_text):
        raise requests.exceptions.HTTPError("fake HTTP error")


def test_successful_provider():
    runner = PromptRunner(SuccessProvider())

    prompt = Prompt(
        prompt_id=1,
        text="What is AI?"
    )

    result = runner.run(
        prompt,
        run_id=1
    )

    assert result.prompt_id == 1
    assert result.run_id == 1
    assert result.response == "test response"


def test_timeout_provider():
    runner = PromptRunner(TimeoutProvider())

    prompt = Prompt(
        prompt_id=1,
        text="test"
    )

    with pytest.raises(requests.exceptions.Timeout):
        runner.run(prompt, run_id=1)


def test_connection_error():
    runner = PromptRunner(ConnectionFailProvider())

    prompt = Prompt(
        prompt_id=1,
        text="test"
    )

    with pytest.raises(requests.exceptions.ConnectionError):
        runner.run(prompt, run_id=1)


def test_http_error():
    runner = PromptRunner(HTTPFailProvider())

    prompt = Prompt(
        prompt_id=1,
        text="test"
    )

    with pytest.raises(requests.exceptions.HTTPError):
        runner.run(prompt, run_id=1)


def test_missing_data_file(tmp_path, monkeypatch):
    fake_file = tmp_path / "does_not_exist.json"

    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        fake_file
    )

    data = storage.load_data()

    assert data == {
        "prompts": [],
        "responses": []
    }


def test_corrupted_json(tmp_path, monkeypatch):
    fake_file = tmp_path / "data.json"

    fake_file.write_text(
        "{ broken json",
        encoding="utf-8"
    )

    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        fake_file
    )

    with pytest.raises(ValueError):
        storage.load_data()


def test_invalid_prompt_data(tmp_path, monkeypatch):
    fake_file = tmp_path / "data.json"

    bad_data = {
        "prompts": [
            {
                "id": 1,
                "text": ""
            }
        ],
        "responses": []
    }

    fake_file.write_text(
        json.dumps(bad_data),
        encoding="utf-8"
    )

    monkeypatch.setattr(
        storage,
        "DATA_FILE",
        fake_file
    )

    with pytest.raises(ValueError):
        storage.load_data()


def test_timing_decorator_returns_original_result():

    @Time_Taken
    def example():
        return "hello"

    result = example()

    assert result == "hello"