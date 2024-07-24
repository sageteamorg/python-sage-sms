"""
Phone Number Validation and Formatting Module

This module contains the PhoneNumberValidator class, responsible for
validating and formatting phone numbers using the `phonenumbers` library.

Classes:
    - PhoneNumberValidator: Class for validating and formatting phone numbers.

Exceptions:
    - ImportError: Raised when the `phonenumbers` package is not installed.

Usage:
    validator = PhoneNumberValidator()
    formatted_number = validator.validate_and_format("+1 650-253-0000")

Example:
    >>> validator = PhoneNumberValidator()
    >>> formatted_number = validator.validate_and_format("+1 650-253-0000")
    >>> print(formatted_number)
    '+16502530000'
"""

try:
    import phonenumbers
except ImportError:
    phonenumbers = None


class PhoneNumberValidator:
    """
    PhoneNumberValidator Class

    Responsible for validating and formatting phone numbers.

    Methods:
        - validate_and_format: Validates and formats a phone number string.
    """

    def validate_and_format(self, phone_number: str, region: str | None = None) -> str:
        """
        Validate and format a phone number string.

        The method uses the `phonenumbers` library
        to validate and format the phone number.
        The format used is E.164.

        Args:
            phone_number (str): The phone number to validate and format.

        Returns:
            str: The validated and formatted phone number in E.164 format.

        Raises:
            ImportError: Raised when the `phonenumbers` package is not installed.
        """
        if phonenumbers is None:
            raise ImportError(
                "Install `phonenumbers` package. Run `pip install phonenumbers`."
            )
        parsed_number = phonenumbers.parse(phone_number, region)
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
