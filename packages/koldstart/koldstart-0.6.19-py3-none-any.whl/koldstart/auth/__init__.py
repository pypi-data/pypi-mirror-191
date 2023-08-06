from __future__ import annotations

from dataclasses import dataclass, field

import click
from koldstart.auth import auth0, local
from koldstart.console import console
from koldstart.console.icons import CHECKMARK
from rich.text import Text


def login():
    token_data = auth0.login()
    local.save_token(token_data["refresh_token"])


def logout():
    refresh_token = local.load_token()
    if refresh_token is None:
        raise click.ClickException(message="You're not logged in")
    auth0.revoke(refresh_token)
    local.delete_token()
    console.print(f"{CHECKMARK} Logged out of [bold]koldstart[/]")


def _fetch_access_token() -> str:
    """
    Load the refresh token, request a new access_token (refreshing the refresh token)
    and return the access_token.

    TODO: We could do this if the access_token is expired (it lasts 1 day),
    instead of every time we invoke.
    """
    refresh_token = local.load_token()

    if refresh_token is None:
        raise click.ClickException(
            message="You must be authenticated. Use `koldstart auth login`"
        )

    # TODO: avoid refreshing on every call by storing refresh and access token
    # and only refreshing when the access token is invalid
    try:
        token_data = auth0.refresh(refresh_token)
    except click.ClickException:
        local.delete_token()
        raise

    # NOTE: Auth0 Refresh Token Rotation enabled
    # So the old refresh_token is no longer valid
    local.save_token(token_data["refresh_token"])

    return token_data["access_token"]


@dataclass
class UserAccess:
    _access_token: str | None = field(repr=False, default=None)
    _user_info: dict | None = field(repr=False, default=None)

    @property
    def info(self) -> dict:
        if self._user_info is None:
            self._user_info = auth0.get_user_info(self.bearer_token)

        return self._user_info

    @property
    def access_token(self) -> str:
        if self._access_token is None:
            self._access_token = _fetch_access_token()

        return self._access_token

    @property
    def bearer_token(self) -> str:
        return "Bearer " + self.access_token


USER = UserAccess()
