from typing import TypedDict, Any

try:
    from typing import override
except ImportError:  # for Python < 3.12
    from overrides import override

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Response,
)
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam


class ParameterSpec(TypedDict):
    api_key: str
    model: str
    system_prompt: str
    temperature: float
    top_p: float
    max_tokens: int


class GPTAnswerProvider(BaseAnswerProvider[ParameterSpec]):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.client = OpenAI(api_key=self.settings["api_key"])

    @override
    def answer(
        self,
        message: str,
        history: list[str] | None = None,
        custom_system_prompt: str | None = None,
    ) -> Response:
        message_list = self.build_message_list(
            message, history or [], custom_system_prompt
        )
        args = dict(model=self.settings["model"], messages=message_list, n=1)
        for k in ["temperature", "top_p", "max_tokens"]:
            v = self.settings.get(k, None)
            if v:
                args[k] = v
        completion = self.client.chat.completions.create(**args)
        answer = completion.choices[0].message.content
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
    ) -> list[ChatCompletionMessageParam]:
        messages: list[ChatCompletionMessageParam] = []

        if custom_system_prompt is not None:
            system_prompt = custom_system_prompt
        else:
            system_prompt = self.get_default_system_prompt()
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        from_user = True
        for message in history:
            messages.append(
                {
                    "role": "user" if from_user else "assistant",
                    "content": self.settings["system_prompt"],
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
