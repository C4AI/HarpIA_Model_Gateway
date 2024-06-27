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
parser.add_argument("--mode", choices=["server", "cli"], default="server")
parser.add_argument("--provider", type=str)
args = parser.parse_args()

service = AnswerProviderService(args.config)
match args.mode:
    case "server":
        service.serve()
    case "cli":
        if not args.provider:
            parser.error("--mode=cli requires --provider")
        else:
            service.cli(args.provider)
