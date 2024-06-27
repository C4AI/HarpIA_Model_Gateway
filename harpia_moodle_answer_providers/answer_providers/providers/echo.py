from typing import TypedDict

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Response,
)


class ParameterSpec(TypedDict):
    to_uppercase: bool


class EchoAnswerProvider(BaseAnswerProvider[ParameterSpec]):

    def answer(self, message: str) -> Response:
        text = message
        if self.settings["to_uppercase"]:
            text = text.upper()
        return Response(
            text=text,
            contexts=[],
            interaction_id=self.generate_id(),
        )
