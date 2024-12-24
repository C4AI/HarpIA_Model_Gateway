from typing import TypedDict

try:
    from typing import override
except ImportError:  # for Python < 3.12
    from overrides import override


from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Response,
)


class ParameterSpec(TypedDict):
    to_uppercase: bool


class EchoAnswerProvider(BaseAnswerProvider[ParameterSpec]):

    @override
    def answer(
        self,
        message: str,
        history: list[str] | None = None,
        custom_system_prompt: str | None = None,
    ) -> Response:
        if custom_system_prompt:
            msg = "{self.__class__} does not support system prompts"
            raise ValueError(msg)
        text = message
        if self.settings["to_uppercase"]:
            text = text.upper()
        return Response(
            text=text,
            contexts=[],
            interaction_id=self.generate_id(),
        )

    @classmethod
    def supports_system_prompt(cls) -> bool:
        return False
