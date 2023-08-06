from rich.console import Console

from patch.auth.auth_client import AuthClient, AuthResponseStatus
from patch.storage.auth import AuthPayload
from patch.storage.storage import Storage
from patch.tp.phone_number import PhoneNumber


class AuthPhoneNumber:
    """
    The class is responsible for authentication via phone number.
    It is outdated procedure, that involves deprecated DGraph endpoints.
    The procedure will be replaced by a direct FusionAuth calls.
    """

    def __init__(self, phone_number: PhoneNumber):
        self._phone_number = phone_number
        self.console = Console()
        self._ac = AuthClient()

    def request_validation(self):
        result = self._ac.login_or_signup(self._phone_number.canonical)
        self._handle_response(result)

    def _handle_response(self, result):
        status = result.status
        if status == AuthResponseStatus.Pending:
            channel = result.verification.channel
            if channel == 'sms':
                self._respond_pending_sms(result)
            else:
                self._respond_problem('Unknown verification type')
        elif status == AuthResponseStatus.Failure:
            self._respond_problem(result.error)
        elif status == AuthResponseStatus.Success:
            access_token = result.token
            refresh_token = result.refresh_token
            self._respond_success(access_token, refresh_token)

    def _respond_pending_sms(self, result):
        dest_phone = result.verification.to
        self.console.print(f"Check SMS on [blue]{dest_phone}[/blue] for the confirmation code")
        code = self.console.input("[yellow]Code> [/yellow]")
        response = self._ac.validate_phone(self._phone_number.canonical, code)
        self._handle_response(response)

    def _respond_problem(self, error):
        self.console.print(f"There is a problem: [red]{error}[/red]")

    def _respond_success(self, access_token, refresh_token):
        storage = Storage()
        storage.auth.store(AuthPayload(access_token=access_token, refresh_token=refresh_token))
        self.console.print('[green]Authentication succeeded[/green]')
