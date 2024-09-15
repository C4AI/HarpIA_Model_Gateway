import argparse
import logging
from pathlib import Path

from harpia_moodle_answer_providers.server import AnswerProviderService

logging.basicConfig()


def config_type(fn: str) -> Path:
    p = Path(fn)
    if p.suffix != ".py":
        msg = "Invalid extension: " + p.suffix.lstrip(".")
        raise argparse.ArgumentTypeError(msg)
    if not p.is_file():
        msg = "Configuration file not found"
        raise argparse.ArgumentTypeError(msg)
    return p


parser = argparse.ArgumentParser(description="HarpIA Answer Providers")
parser.add_argument(
    "--config",
    type=config_type,
    help="Path to the configuration file (.py)",
    required=True,
)
subparsers = parser.add_subparsers(dest="mode", required=True)

server_subparser = subparsers.add_parser("server")
server_subparser.add_argument("--host", type=str, required=True)
server_subparser.add_argument("--port", type=int, required=True)
server_subparser.add_argument("--debug", "-d", action="store_true")


cli_subparser = subparsers.add_parser("cli")
cli_subparser.add_argument("--provider", type=str, required=True)

args = parser.parse_args()

service = AnswerProviderService(args.config)
match args.mode:
    case "server":
        service.serve(args.host, args.port, args.debug)
    case "cli":
        if not args.provider:
            parser.error("--mode=cli requires --provider")
        else:
            service.cli(args.provider)
