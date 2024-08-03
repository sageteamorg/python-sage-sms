# python-sage-sms

The Sage SMS package is designed to facilitate the sending of SMS messages through various providers. This package provides a flexible and extensible framework for integrating multiple SMS backends, validating phone numbers, and handling SMS-related errors.

## Key Features

- **Modular Design**: The package is organized into modules for different functionalities, including backend management, phone number validation, and exception handling.
- **Backend Discovery and Loading**: SMS backends are dynamically discovered and loaded based on the provided configuration.
- **Phone Number Validation**: Phone numbers are validated and formatted using the `phonenumbers` library to ensure compliance with international standards.
- **Exception Handling**: Custom exceptions are defined for various error scenarios, providing clear and specific error messages.

## Getting Started

### Installation

To install the Sage SMS package, use pip:

```bash
pip install python-sage-sms
```

### Usage

To use an SMS backend, import the necessary modules and configure the settings for the desired SMS provider. Here is a quick example:

```python
from sage_sms.factory import SMSBackendFactory

# Define settings for the SMS provider
settings = {
    "debug": False,
    "provider": {
        "NAME": "provider_name",
        "API_KEY": "your_api_key"
    }
}

# Initialize the factory with settings and the base package path for the backends
# Replace "your_project.backends" with the actual path where your backend modules are located
factory = SMSBackendFactory(settings, "your_project.backends")

# Get the SMS provider class and instantiate it
sms_provider_class = factory.get_backend()
sms_provider = sms_provider_class(settings)

# Send a test SMS message
sms_provider.send_one_message("+1234567890", "Hello, World!")
```

## Creating a Backend

To create a new SMS backend, follow these steps:

1. **Implement the ISmsProvider Interface**: Create a class that implements the methods defined in the `ISmsProvider` interface.
2. **Add Backend Module**: Add the new backend module to the appropriate package directory.
3. **Update Configuration**: Update the configuration settings to include the new backend provider.

### Example: Twilio Backend

Here is an example of how to implement a backend for the Twilio service.

```python
import logging
logger = logging.getLogger(__name__)

try:
    from twilio.rest import Client as TwilioClient
except ImportError:
    TwilioClient = None
    logger.error("Failed to import TwilioClient. Ensure 'twilio' package is installed.")

from sage_sms.design.interfaces.provider import ISmsProvider
from sage_sms.validators import PhoneNumberValidator

class Twilio(ISmsProvider):
    def __init__(self, settings):
        if TwilioClient is None:
            logger.critical(
                "TwilioClient is None. Install `twilio` package. Run `pip install twilio`."
            )
            raise ImportError(
                "Install `twilio` package. Run `pip install twilio`."
            )

        self.phone_number_validator = PhoneNumberValidator()
        self._api_key = settings["provider"]["API_KEY"]
        self._auth_token = settings["provider"]["AUTH_TOKEN"]
        self._line_number = settings["provider"].get("LINE_NUMBER")
        self.twilio_client = TwilioClient(self._api_key, self._auth_token)

    def send_one_message(self, phone_number: str, message: str, linenumber=None) -> None:
        try:
            cast_phone_number = self.phone_number_validator.validate_and_format(phone_number, region="US")
            self.twilio_client.messages.create(
                from_=self._line_number,
                body=message,
                to=cast_phone_number
            )
        except Exception as e:
            logger.error(f"Failed to send message to {phone_number}: {e}")

    def send_bulk_messages(self, phone_numbers: list[str], message: str, linenumber=None) -> None:
        raise NotImplementedError

    def send_verify_message(self, phone_number: str, value: str):
        raise NotImplementedError
```

## Conclusion

The Sage SMS package offers a robust and flexible solution for sending SMS messages through various providers. Its modular design, comprehensive validation, and detailed error handling make it a reliable choice for integrating SMS functionality into applications.

For detailed instructions on creating backends, read the [Creating a Backend](https://python-sage-sms.readthedocs.io/en/latest/) section in the documentation.
