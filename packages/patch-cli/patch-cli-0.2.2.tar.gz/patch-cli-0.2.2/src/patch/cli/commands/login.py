import click

from patch.auth.auth_phone_number import AuthPhoneNumber
from patch.cli.phone_number_param_type import PhoneNumberParamType
from patch.cli.styled import StyledCommand
from patch.tp.phone_number import PhoneNumber


@click.command(cls=StyledCommand, help='Login to Patch using your mobile phone')
@click.argument('phone', type=PhoneNumberParamType())
def login(phone: PhoneNumber):
    auth = AuthPhoneNumber(phone)
    auth.request_validation()
