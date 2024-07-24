"""
smsir.py
=========
This module provides an implementation for the ISmsProvider interface,
specifically tailored
for sending SMS via the SMS_IR service.

Dependencies:
    - `sms_ir` library, installed as SmsIRLib
    - PhoneNumberValidator for phone number validation

Example:
    >>> sms_provider = SmsIr(api_key="Your-API-Key")
    >>> sms_provider.send_one_message("+1234567890", "Hello, World!")
"""

try:
    from sms_ir import SmsIr as SmsIRLib
except ImportError:
    SmsIRLib = None

from ..design.interfaces.provider import ISmsProvider
from ..validators import PhoneNumberValidator


class SmsIr(ISmsProvider):
    """
    smsir class implementing the ISmsProvider interface
    for sending SMS via smsir service.

    Attributes:
        api_key (str): The API key for smsir service.
        linenumber (str): The line number used for sending SMS.
    """

    def __init__(self, settings):
        """
        Initializes smsir with the given API key and line number.

        Args:
            api_key (str): The API key for smsir.

        Raises:
            ImportError: If the `smsir` or `requests` package is not installed.
        """
        if SmsIRLib is None:
            raise ImportError("Install `smsir`, Run `pip install smsir`.")

        self.phone_number_validator = PhoneNumberValidator()
        self._api_key = settings["provider"]["API_KEY"]
        self._line_number = settings["provider"].get("LINE_NUMBER")
        self.smsir = SmsIRLib(self._api_key)

    def send_one_message(
        self, phone_number: str, message: str, linenumber=None
    ) -> None:
        """
        Sends a single SMS message.

        Args:
            phone_number (str): The recipient's phone number.
            message (str): The message text.
        """
        cast_phone_number = self.phone_number_validator.validate_and_format(
            phone_number, region="IR"
        )
        self.smsir.send_sms(cast_phone_number, message, self._line_number)

    def send_bulk_messages(
        self, phone_numbers: list[str], message: str, linenumber=None
    ) -> None:
        """
        Sends an SMS message to multiple recipients.

        Args:
            phone_numbers (list[str]): List of recipient phone numbers.
            message (str): The message text.
        """
        parsed_numbers = [
            self.phone_number_validator.validate_and_format(number)
            for number in phone_numbers
        ]
        self.smsir.send_bulk_sms(parsed_numbers, message, self._line_number)

    def send_verify_message(self, phone_number: str, value: str):
        """
        Send a verification message.

        Args:
            phone_number (str): The recipient's phone number.
            value (str): The verification code or value.
        """
