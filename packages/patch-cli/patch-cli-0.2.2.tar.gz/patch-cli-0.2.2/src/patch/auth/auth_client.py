import json
import os
from enum import Enum
from typing import Optional

import requests
from dataclasses import dataclass, field

from requests import HTTPError

from patch.auth.auth_token import global_access_token


class AuthResponseStatus(Enum):
    Success = 'Success',
    Failure = 'Failure'
    Pending = 'Pending'


@dataclass
class AuthResponse:
    status: AuthResponseStatus = field(init=False)


@dataclass
class AuthResponseFailure(AuthResponse):
    error: str

    def __post_init__(self):
        self.status = AuthResponseStatus.Failure


@dataclass
class AuthResponsePendingVerification:
    to: str
    channel: str


@dataclass
class AuthResponsePending(AuthResponse):
    verification: AuthResponsePendingVerification

    def __post_init__(self):
        self.status = AuthResponseStatus.Pending


@dataclass
class AuthResponseSuccess(AuthResponse):
    token: str
    refresh_token: str

    def __post_init__(self):
        self.status = AuthResponseStatus.Success


class AuthClient:
    DEFAULT_AUTH_URL: str = 'https://api.patch.tech/v1'

    def __init__(self, auth_url=None):
        self._auth_url = auth_url or os.environ.get('PATCH_AUTH_URL') or AuthClient.DEFAULT_AUTH_URL

    def login_or_signup(self, phone):
        try:
            result = self.call_post('/auth/login', phone=phone)
            body = result.json()
            status = body.get('result', None)
            if status == 'OK':
                return AuthResponsePending(verification=AuthResponsePendingVerification(to=phone, channel='sms'))
            else:
                return AuthResponseFailure(error=f"Error: Auth server returned status #{status}")
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def validate_phone(self, phone, code):
        try:
            result = self.call_post('/auth/login/verify/sms', phone=phone, code=code)
            body = result.json()
            token = body['token']
            refresh_token = body['refreshToken']
            return AuthResponseSuccess(token=token, refresh_token=refresh_token)
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            return AuthResponseFailure(error=f"Error: {message}")

    def call_refresh(self, current_refresh):
        try:
            result = self.call_post('/auth/refresh', refreshToken=current_refresh)
            return result.json()
        except HTTPError as e:
            message = e.response.json().get('message', None) \
                      or f"Auth server responded with HTTP code {e.response.status_code}"
            raise Exception(f"Error: {message}")

    def call_post(self, path, **kwargs):
        headers = {"Content-Type": "application/json"}
        response = requests.post(self._auth_url + path, data=json.dumps(kwargs), headers=headers, allow_redirects=True)
        response.raise_for_status()
        return response

    def get_access_token(self) -> Optional[str]:
        if global_access_token and global_access_token.has_token():
            if global_access_token.needs_refresh():
                token_payload = self.call_refresh(global_access_token.get_refresh())
                new_access_token = token_payload['token']
                refresh_token = token_payload['refreshToken']
                global_access_token.store(new_access_token, refresh_token)
                return new_access_token
            else:
                return global_access_token.get_access_token()
