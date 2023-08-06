from bioto_client.domain.users import User, UserException, Users
import os


class UsersSessionStorage(Users):
    env_file: str

    def __init__(self, env: str = "prod") -> None:
        self.env_file = f".session.{env}"

    def clear(self) -> None:
        self.store(User())

    def load(self) -> User:
        access_token = os.getenv("ACCESS_TOKEN")

        if access_token is None:
            lines = self._read_env_file()

            for line in lines:
                if "ACCESS_TOKEN" in line:
                    access_token = line.split("\"")[1].strip()

        if access_token is None or access_token == "":
            raise UserException("No user session available, please login")

        return User(name="", access_token=access_token)

    def store(self, user: User) -> None:
        # Remove session token from env when not set
        if user.access_token is None:
            if os.getenv("ACCESS_TOKEN"):
                del os.environ["ACCESS_TOKEN"]
            access_token_line = "ACCESS_TOKEN=\"\""
        else:
            os.environ["ACCESS_TOKEN"] = user.access_token
            access_token_line = f"ACCESS_TOKEN=\"{user.access_token}\""

        lines = self._read_env_file()

        replaced = False
        for index, line in enumerate(lines):
            if "ACCESS_TOKEN" in line:
                lines[index] = access_token_line
                replaced = True
            else:
                lines[index] = line.strip()

        if not replaced:
            lines.append(access_token_line)

        self._write_env_file(lines)

    def _read_env_file(self) -> list[str]:
        try:
            file = open(self.env_file, "r")
            lines = file.readlines()
            file.close()
        except FileNotFoundError:
            lines = []

        return lines

    def _write_env_file(self, lines: list[str]) -> None:
        file = open(self.env_file, "w+")
        file.write("\n".join(lines))
        file.close()
