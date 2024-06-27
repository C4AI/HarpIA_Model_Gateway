from dataclasses import asdict
from pathlib import Path

from flask import Flask, jsonify, request

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Request,
    Response,
)
from harpia_moodle_answer_providers.cfg_reader import load_configuration


class AnswerProviderService:

    def __init__(self, config_path: Path):
        self.config = load_configuration(config_path)
        self.providers: dict[str, BaseAnswerProvider] = {}
        for item in self.config.ANSWER_PROVIDERS:
            cls = BaseAnswerProvider.find_model(item["class"])
            self.providers[item["name"]] = cls(item["settings"])

    def send_message(self, req: Request) -> Response:
        provider = self.providers.get(req.answer_provider)
        output = provider.answer(req.text)
        return Response(
            text=output.text,
            contexts=output.contexts,
            interaction_id=output.interaction_id,
        )

    def serve(self):

        app = Flask(__name__)

        @app.route("/send", methods=["POST"])
        def send_message():
            j = request.json
            req = Request(text=j["query"], answer_provider=j["answer_provider"])
            resp = self.send_message(req)
            return jsonify(asdict(resp))

        @app.route("/list", methods=["GET"])
        def list_providers():
            return jsonify({"providers": [*self.providers.keys()]})

        app.run(host="0.0.0.0", port=42774)

    def cli(self, answer_provider: str) -> None:

        import colorama  # noqa: F401
        import readline  # noqa: F401

        while True:
            try:
                question = input(colorama.Style.RESET_ALL + colorama.Style.DIM + "> ")
            except (KeyboardInterrupt, EOFError):
                return
            if not question:
                continue
            req = Request(text=question, answer_provider=answer_provider)
            resp = self.send_message(req)
            print(
                colorama.Style.RESET_ALL + colorama.Style.BRIGHT + f"\n{resp.text}\n\n"
            )
