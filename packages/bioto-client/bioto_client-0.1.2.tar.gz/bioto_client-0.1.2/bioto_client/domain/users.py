from abc import ABC, abstractmethod
from pydantic import BaseModel


class User(BaseModel):
    name: str = None
    access_token: str = None


class UserException(Exception):
    pass


class Users(ABC):
    @abstractmethod
    def clear(self) -> User:
        """Remove user session from storage"""
        raise NotImplementedError()

    @abstractmethod
    def load(self) -> User:
        """Load active user from storage"""
        raise NotImplementedError()

    @abstractmethod
    def store(self, user: User) -> None:
        """Persist given user to storage"""
        raise NotImplementedError()
