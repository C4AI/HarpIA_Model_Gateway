from datetime import datetime
from uuid import uuid4
from abc import ABCMeta, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from importlib import util as import_util
from pathlib import Path
from typing import TypeVar, Mapping, Any, Self, Generic


@dataclass
class Request:
    text: str
    answer_provider: str


@dataclass
class ResponseContext:
    text: str


@dataclass
class Response:
    text: str
    contexts: list[ResponseContext]
    interaction_id: str


InputT = TypeVar("InputT", bound=Mapping[str, Any])


class BaseAnswerProvider(Generic[InputT], metaclass=ABCMeta):

    __subclasses: dict[str, type[Self]] = {}

    __imported_all = False

    def __init__(self, settings: InputT):
        self.settings = settings

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__name__
        assert name not in cls.__subclasses, f"Duplicate model class name: {name}"
        cls.__subclasses[name] = cls

    @classmethod
    def __import_all(cls) -> None:
        if cls.__imported_all:
            return
        cls.__imported_all = True
        for module in Path(__file__).parent.rglob("*.py"):
            if not module.name.startswith("_"):
                spec = import_util.spec_from_file_location(module.name[:-3], module)
                if not spec or not spec.loader:
                    error = "Could not load {module.name}"
                    raise ValueError(error)
                spec.loader.exec_module(import_util.module_from_spec(spec))
        del module

    @classmethod
    def answer_providers(cls) -> Sequence[str]:
        cls.__import_all()
        return [*cls.__subclasses.keys()]

    @classmethod
    def find_model(cls, class_name: str) -> type[Self] | None:
        cls.__import_all()
        return cls.__subclasses.get(class_name, None)

    @abstractmethod
    def answer(self, message: str) -> Response: ...

    def generate_id(self) -> str:
        fmt = "%Y%m%d_%H%M%S_%f_"
        return datetime.now().strftime(fmt) + str(uuid4()).replace("-", "")
