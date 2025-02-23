from typing import TypedDict, Any

try:
    from typing import override
except ImportError:  # for Python < 3.12
    from overrides import override

import requests

from harpia_model_gateway.answer_providers.providers.base import (
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
        self.pulled = False

    @override
    def answer(
        self,
        message: str,
        history: list[str] | None = None,
        custom_system_prompt: str | None = None,
    ) -> Response:
        if not self.pulled:
            requests.post(
                self.settings["ollama_address"] + "/pull",
                json={"model": self.settings["model"]},
            )
            self.pulled = True
        message_list = self.build_message_list(
            message, history or [], custom_system_prompt
        )
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

    def build_message_list(
        self,
        message: str,
        history: list[str],
        custom_system_prompt: str | None = None,
    ) -> list[dict[str, Any]]:
        messages = []

        if custom_system_prompt:
            system_prompt = custom_system_prompt
        else:
            system_prompt = self.get_default_system_prompt()
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        from_user = True
        for msg in history:
            messages.append(
                {
                    "role": "user" if from_user else "assistant",
                    "content": msg,
                }
            )
            from_user = not from_user
        messages.append({"role": "user", "content": message})
        return messages

    def get_default_system_prompt(self) -> str:
        return self.settings.get("default_system_prompt", None)

    @classmethod
    @override
    def supports_system_prompt(cls) -> bool:
        return True
