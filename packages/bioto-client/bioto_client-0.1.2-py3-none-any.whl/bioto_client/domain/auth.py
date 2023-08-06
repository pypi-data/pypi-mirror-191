from abc import ABC, abstractmethod
from bioto_client.domain.users import User


class AuthError(Exception):
    pass


class SessionExpired(Exception):
    pass


class Auth(ABC):

    @abstractmethod
    def login(self) -> User:
        """Login to external service and return a User"""
        raise NotImplementedError()
