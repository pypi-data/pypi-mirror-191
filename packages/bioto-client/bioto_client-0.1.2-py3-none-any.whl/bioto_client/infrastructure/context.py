from dotenv import dotenv_values
from bioto_client.domain.auth import Auth
from bioto_client.domain.repository import Repository
from bioto_client.domain.users import User, Users
from bioto_client.infrastructure.auth.auth0 import Auth0
from bioto_client.infrastructure.repository.api import Api
from bioto_client.infrastructure.users.users_session_storage \
    import UsersSessionStorage
import os


class Context():
    env: str
    config: list[str]
    auth: Auth = None
    users: Users = None
    repository: Repository = None

    def __init__(self):
        # Config should default to production settings
        env = os.getenv("ENV", "prod").strip() or "prod"
        if env not in ["test", "dev", "prod"]:
            raise RuntimeError(f"Invalid ENV '{env}'")

        self.env = env

        # Assume production settings...
        self.config = {
            "algorithms": ["RS256"],
            "audience": "https://api.bioto.co",
            "AUTH0_DOMAIN": "https://biotoco.eu.auth0.com",
            "AUTH0_CLIENT": "iMynqN5DyJHFyJRLCLkTsAR3cqrj2EtE",
            "BASE_ENDPOINT": "api.bioto.co",
            "ENV": env
        }

        # ... which can be overwritten by a specific .env file
        if env != "prod":
            self.config.update(dotenv_values(f".env.{env}"))

    def get_auth_service(self) -> Auth:
        if self.auth:
            return self.auth

        if self.env in ["dev", "prod"]:
            return Auth0(self.config)

        raise RuntimeError("No auth service set")

    def get_repository(self, user: User) -> Repository:
        if self.repository:
            return self.repository

        self.repository = Api(user, self.config)

        return self.repository

    def get_users_service(self) -> Users:
        if self.users:
            return self.users

        self.users = UsersSessionStorage(self.env)

        return self.users


context = Context()
