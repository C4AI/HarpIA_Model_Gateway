#!/usr/bin/env python3
"""HarpIA Model Gateway entry point."""

from pathlib import Path
from runpy import run_module
from sys import path

path.insert(0, str(Path(__file__).parent / "src"))

run_module("harpia_model_gateway")

