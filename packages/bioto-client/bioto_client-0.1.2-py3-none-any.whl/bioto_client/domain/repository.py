from abc import ABC, abstractmethod
from pydantic import BaseModel
from requests import Response


class NotFound(Exception):
    pass


class Garden(BaseModel):
    name: str


class Repository(ABC):
    @abstractmethod
    def search_garden(self, query: str) -> Response | dict:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self) -> None:
        raise NotImplementedError()
