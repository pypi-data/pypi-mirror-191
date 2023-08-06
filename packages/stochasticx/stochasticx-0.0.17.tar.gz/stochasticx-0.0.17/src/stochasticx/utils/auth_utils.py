import os
import json
import time

import requests
import sys
import click
from pathlib import Path
import uuid

from stochasticx.constants.urls import CloudRoutes, TOKEN_AUTH_PATH, get_cloud_url

WAIT_TOKEN_TIME = 60
BEFORE_RETRY = 2


class OAuth2Links:
    user_link = "https://api.stochastic.ai/v1/auth/google?clientId={}"
    token_link = "https://api.stochastic.ai/v1/auth/cli-login?clientId={}"


class LoginUtils:
    @staticmethod
    def login_request(username, password):
        """Private method to do the login request

        Args:
            username (str): username
            password (str): password

        Returns:
            str: token
        """
        login_info = {"email": username, "password": password}

        response = requests.post(get_cloud_url(CloudRoutes.LOGIN_URL), data=login_info)
        try:
            response.raise_for_status()
        except:
            click.secho("[+] Your credentials are incorrect.\n", fg="red", bold=True)
            sys.exit()

        response_data = response.json()
        token = response_data["token"]

        LoginUtils.save_token(token)

        return token

    @staticmethod
    def link_login_request():
        uuid_string = str(uuid.uuid4())

        click.secho(OAuth2Links.user_link.format(uuid_string), fg="blue")

        click.secho("Receiving your token...", fg="green")

        token = None

        def not_successful():
            click.secho("[+] Failed to get token, try again.\n", fg="red", bold=True)
            sys.exit()

        for _ in range(WAIT_TOKEN_TIME // BEFORE_RETRY):
            try:
                response = requests.get(OAuth2Links.token_link.format(uuid_string))

                if response.status_code == 200:
                    token_json = response.json()

                    if len(token_json) == 0:
                        time.sleep(BEFORE_RETRY)
                        continue

                    token = token_json["token"]

                    break

            except Exception as e:
                not_successful()

        if token is None:
            not_successful()

        # here query for /user/me to get the email (username), token in header
        response = requests.get(
            get_cloud_url(CloudRoutes.ME_URL),
            headers={
                'Authorization': 'Bearer ' + token
            }
        )
        os.environ["STOCHASTIC_USER"] = response.json().get("email")
        LoginUtils.save_token(token)

        return token

    @staticmethod
    def save_token(token):
        # Save token in ENV var
        session = str(uuid.uuid4())
        os.environ["SESSION_STRING"] = session
        os.environ["STOCHASTIC_TOKEN"] = token
        # Save token in a file
        token_path = Path(TOKEN_AUTH_PATH).resolve()
        if not token_path.exists():
            token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(str(token_path), "w", encoding="utf-8") as f:
            json.dump(
                {
                    "token": token,
                    "session": session,
                    "user": os.environ.get("STOCHASTIC_USER"),
                },
                f,
                ensure_ascii=False,
                indent=4,
            )


class AuthUtils:
    @staticmethod
    def get_auth_headers():
        """Get authentication headers from the webapp

        Raises:
            ValueError: if token not found in the following ENV variable STOCHASTIC_TOKEN

        Returns:
            dict: auth headers
        """
        token = os.getenv("STOCHASTIC_TOKEN")
        session_string = os.getenv("SESSION_STRING")

        if token is None or session_string is None:
            if Path(TOKEN_AUTH_PATH).exists():
                f = open(TOKEN_AUTH_PATH)
                data = json.load(f)
                token = data["token"]
                session_string = data.get("session")
                #os.environ["STOCHASTIC_USER"] = data.get("user")

        os.environ["SESSION_STRING"] = session_string

        if token is not None:
            try:
                response = requests.get(
                    get_cloud_url(CloudRoutes.ME_URL),
                    headers={"Authorization": "Bearer " + token},
                )
                response.raise_for_status()
            except:
                click.secho(
                    "[+] You are not logged in. Please execute:", fg="red", bold=True
                )
                click.secho("\n     stochasticx login \n", bold=True)

                sys.exit()

        else:
            click.secho("[+] You are not logged in. Please try:", fg="red", bold=True)
            click.secho("\n     stochasticx login \n", bold=True)
            click.secho(
                "[+] You can sign up for a free account at: https://app.stochastic.ai/signup"
            )

            sys.exit()

        return {"Authorization": "Bearer " + token}


    @staticmethod
    def is_logged_in():
        """Check if user is logged in

        Returns:
            bool: True if user is logged in, False otherwise
        """
        token_path = Path(TOKEN_AUTH_PATH).resolve()
        return token_path.exists()
