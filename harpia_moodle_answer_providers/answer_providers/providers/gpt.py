from typing import TypedDict, Any

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

    def answer(self, message: str) -> Response:
        message_list = self.build_message_list(message)
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

    def build_message_list(self, message: str) -> list[ChatCompletionMessageParam]:
        messages: list[ChatCompletionMessageParam] = []
        if self.settings["system_prompt"]:
            messages.append(
                {"role": "system", "content": self.settings["system_prompt"]}
            )
        messages.append({"role": "user", "content": message})
        return messages
