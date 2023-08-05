from bioto_client.domain.auth import Auth, AuthError
from bioto_client.domain.users import User
from jwt import decode, exceptions, PyJWKClient
import requests
import time
from typing import Any


class Auth0(Auth):
    config: list[str]
    jwks_client: PyJWKClient

    def __init__(self, config: list[str]) -> None:
        self.config = config

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f"{self.config['AUTH0_DOMAIN']}/.well-known/jwks.json"
        self.jwks_client = PyJWKClient(jwks_url)

    def login(self) -> User:
        device_code_data = self.get_device_code_data()

        print(
            '1. On your computer or mobile device navigate to: ',
            device_code_data['verification_uri_complete']
        )
        print('2. Enter the following code: ', device_code_data['user_code'])

        token = self.poll_authentication(
            device_code_data['device_code'],
            device_code_data['interval'],
        )

        self.verify(token["access_token"])

        access_token = token["access_token"]

        user_data = self.get_user_info(access_token)
        user = User(name=user_data["name"], access_token=access_token)

        return user

    def get_device_code_data(self) -> list[str]:
        """
        Runs the device authorization flow
        """
        response: requests.Response = requests.post(
            f"{self.config['AUTH0_DOMAIN']}/oauth/device/code",
            data={
                "client_id": self.config['AUTH0_CLIENT'],
                "scope": "openid profile",
                "audience": self.config['audience']
            }
        )

        if response.status_code != 200:
            raise RuntimeError("Error generating device code")

        return response.json()

    def poll_authentication(self, device_code: str, interval: float = 5) \
            -> list[str]:
        pending_states = ("authorization_pending", "slow_down")
        """
        Polls authentication state until succesful or failed for the given
        interval. Raises a Runtime exception on error or the token data on
        succes.
        """
        token_payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": self.config['AUTH0_CLIENT']
        }

        authenticated = False
        while not authenticated:
            token_response = requests.post(
                f"{self.config['AUTH0_DOMAIN']}/oauth/token",
                data=token_payload
            )

            token_data = token_response.json()
            if token_response.status_code == 200:
                authenticated = True
            elif token_data['error'] not in pending_states:
                raise RuntimeError(token_data['error_description'])
            else:
                time.sleep(interval)

        return token_data

    def verify(self, token: str) -> dict[str, Any]:
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                token
            ).key
        except exceptions.PyJWTError as error:
            raise AuthError(str(error), 400)

        try:
            return decode(
                token,
                self.signing_key,
                algorithms=self.config['algorithms'],
                audience=self.config['audience'],
                issuer=f"{self.config['AUTH0_DOMAIN']}/",
            )
        except Exception as error:
            raise AuthError(str(error), 400)

    def get_user_info(self, access_token: str) -> dict[str]:
        response = requests.post(
            f"{self.config['AUTH0_DOMAIN']}/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if response.status_code != 200:
            raise AuthError(f"Retrieving user info failed: {response.reason}")

        return response.json()
