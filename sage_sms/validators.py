from typing import Any, Optional

try:
    import phonenumbers
except ImportError:
    phonenumbers = None


class PhoneNumberDescriptor:
    """
    Descriptor class for phone number validation and formatting.

    Args:
        name (str): The name of the phone number attribute.
        region (Optional[str]): The region code for phone number parsing.
    """

    def __init__(self, name: str, region: Optional[str] = None) -> None:
        self.name: str = name
        self.region: Optional[str] = region

    def __get__(self, instance: Any, owner: Any) -> str:
        value = instance.__dict__.get(self.name)
        if value is None:
            raise ValueError(f"{self.name} is not set.")
        return value

    def __set__(self, instance: Any, value: str) -> None:
        if phonenumbers is None:
            raise ImportError(
                "Install `phonenumbers` package. Run `poetry add phonenumbers`."
            )
        parsed_number = phonenumbers.parse(value, self.region)
        formatted_number = phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
        instance.__dict__[self.name] = formatted_number

    def __delete__(self, instance: Any) -> None:
        raise AttributeError("Cannot delete the attribute.")


class PhoneNumberValidator:
    """
    PhoneNumberValidator Class

    Responsible for validating and formatting phone numbers.

    Attributes:
        phone_number (PhoneNumberDescriptor): The phone number descriptor.
    """

    phone_number: PhoneNumberDescriptor = PhoneNumberDescriptor("phone_number")

    def __init__(self, phone_number: str, region: Optional[str] = None) -> None:
        self.phone_number: str = phone_number
        self.region: Optional[str] = region

    def validate_and_format(self) -> str:
        """
        Validate and format the phone number.

        The method uses the `phonenumbers` library to validate and format
        the phone number. The format used is E.164.

        Returns:
            str: The validated and formatted phone number in E.164 format.
        """
        return self.phone_number
