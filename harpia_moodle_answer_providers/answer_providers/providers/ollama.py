from typing import TypedDict, Any

import requests

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Response,
)


class ParameterSpec(TypedDict):
    system_prompt: str
    ollama_address: str
    model: str
    extra_ollama_args: dict[str | None] | None


class OllamaAnswerProvider(BaseAnswerProvider[ParameterSpec]):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.settings["extra_ollama_args"] = (
            self.settings.get("extra_ollama_args", None) or {}
        )
        requests.post(
            self.settings["ollama_address"] + "/pull",
            json={"model": self.settings["model"]},
        )

    def answer(self, message: str) -> Response:
        message_list = self.build_message_list(message)
        args = dict(
            **self.settings["extra_ollama_args"],
            model=self.settings["model"],
            messages=message_list,
            stream=False,
        )
        r = requests.post(self.settings["ollama_address"] + "/chat", json=args)
        answer = r.json()["message"]["content"]
        return Response(
            text=answer,
            contexts=[],
            interaction_id=self.generate_id(),
        )

    def build_message_list(self, message: str) -> list[dict[str, Any]]:
        messages = []
        if self.settings["system_prompt"]:
            messages.append(
                {"role": "system", "content": self.settings["system_prompt"]}
            )
        messages.append({"role": "user", "content": message})
        return messages
