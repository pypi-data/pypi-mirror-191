from abc import ABC, abstractmethod
from pydantic import BaseModel


class NotFound(Exception):
    pass


class Garden(BaseModel):
    name: str


class Repository(ABC):
    @abstractmethod
    def search_garden(self, query: str) -> list[Garden]:
        raise NotImplementedError()

    @abstractmethod
    def update_user(self) -> None:
        raise NotImplementedError()
