from typing import TypedDict

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Response,
)

try:
    from typing import override
except ImportError:  # for Python < 3.12
    from overrides import override


class ParameterSpec(TypedDict):
    message: str


class ConstantAnswerProvider(BaseAnswerProvider[ParameterSpec]):

    @override
    def answer(self, message: str) -> Response:
        answer = self.settings["message"]
        return Response(
            text=answer,
            contexts=[],
            interaction_id=self.generate_id(),
        )
