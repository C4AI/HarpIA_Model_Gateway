"""Answer provider service."""

from dataclasses import asdict
from pathlib import Path

from flask import Flask, jsonify, request
from waitress import serve

from harpia_moodle_answer_providers.answer_providers.providers.base import (
    BaseAnswerProvider,
    Request,
    Response,
)
from harpia_moodle_answer_providers.cfg_reader import load_configuration


class AnswerProviderService:
    """Implementation of an answer provider for HarpIA."""

    def __init__(self, config_path: Path):
        """.

        Args:
            config_path: path to the configuration file
        """
        self.config = load_configuration(config_path)
        self.providers: dict[str, BaseAnswerProvider] = {}
        for item in self.config.ANSWER_PROVIDERS:
            cls = BaseAnswerProvider.find_model(item["class"])
            self.providers[item["name"]] = cls(item["settings"])

    def _send_message(self, req: Request) -> Response:
        """Send a message and obtain an answer from the provider.

        Args:
            req: the answer request

        Return:
            the generated answer
        """
        provider = self.providers.get(req.answer_provider)
        output = provider.answer(req.text, req.history, req.system_prompt)
        return Response(
            text=output.text,
            contexts=output.contexts,
            interaction_id=output.interaction_id,
        )

    def serve(self, host: str, port: int, debug: bool) -> None:
        """Start the HTTP server.

        Args:
            host: the host (e.g. 0.0.0.0 = allow all; 127.0.0.1 = allow only local)
            port: port to listen on
            debug: whether debugging mode should be enabled
        """

        app = Flask(__name__)

        @app.route("/send", methods=["POST"])
        def send_message():
            j = request.json
            req = Request(
                text=j["query"],
                answer_provider=j["answer_provider"],
                history=j.get("history", []),
                system_prompt=j.get("system_prompt", None),
            )
            resp = self._send_message(req)
            return jsonify(asdict(resp))

        @app.route("/list", methods=["GET"])
        def list_providers():
            return jsonify(
                {
                    "providers": [
                        {
                            "name": name,
                            "supports_system_prompt": provider.supports_system_prompt(),
                            "default_system_prompt": provider.get_default_system_prompt(),
                        }
                        for name, provider in self.providers.items()
                    ]
                }
            )

        if debug:
            app.run(host=host, port=port, debug=debug)
        else:
            serve(app, host=host, port=port)

    def cli(self, answer_provider: str) -> None:
        """Start a command-line interface.

        Args:
            answer_provider: name of the provider
        """

        import colorama  # noqa: F401

        while True:
            try:
                question = input(colorama.Style.RESET_ALL + colorama.Style.DIM + "> ")
            except (KeyboardInterrupt, EOFError):
                return
            if not question:
                continue
            req = Request(text=question, answer_provider=answer_provider, history=[])
            resp = self._send_message(req)
            print(
                colorama.Style.RESET_ALL + colorama.Style.BRIGHT + f"\n{resp.text}\n\n"
            )
