.. _creating-backends:

How to work with Backends
==========================

To create an SMS backend for the Sage SMS package, follow these steps. This example demonstrates the implementation of backends for the Twilio and SMS_IR providers.

Here are two examples of how to create different backends:

Twilio Backend Implementation
=============================

This section details how to implement the `ISmsProvider` interface for the Twilio service. The backend will enable sending single, bulk, and verification SMS messages.

Module: `twilio.py`
-------------------

The `twilio.py` module provides an implementation for the `ISmsProvider` interface, specifically tailored for sending SMS via the Twilio service.

Dependencies
============

- `twilio` library
- PhoneNumberValidator for phone number validation

Implementation
==============

.. code-block:: python

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

SMS_IR Backend Implementation
=============================

This section details how to implement the `ISmsProvider` interface for the SMS_IR service. The backend will enable sending single, bulk, and verification SMS messages.

Module: `smsir.py`
-------------------

The `smsir.py` module provides an implementation for the `ISmsProvider` interface, specifically tailored for sending SMS via the SMS_IR service.

Dependencies
============

- `sms_ir` library, installed as `SmsIRLib`
- PhoneNumberValidator for phone number validation

Implementation
==============

.. code-block:: python

    try:
        from sms_ir import SmsIr as SmsIRLib
    except ImportError:
        SmsIRLib = None

    from sage_sms.design.interfaces.provider import ISmsProvider
    from sage_sms.validators import PhoneNumberValidator

    class SmsIr(ISmsProvider):
        def __init__(self, settings):
            if SmsIRLib is None:
                raise ImportError("Install `smsir`, Run `pip install smsir`.")

            self.phone_number_validator = PhoneNumberValidator()
            self._api_key = settings["provider"]["API_KEY"]
            self._line_number = settings["provider"].get("LINE_NUMBER")
            self.smsir = SmsIRLib(self._api_key)

        def send_one_message(self, phone_number: str, message: str, linenumber=None) -> None:
            cast_phone_number = self.phone_number_validator.validate_and_format(phone_number, region="IR")
            self.smsir.send_sms(cast_phone_number, message, self._line_number)

        def send_bulk_messages(self, phone_numbers: list[str], message: str, linenumber=None) -> None:
            raise NotImplementedError

        def send_verify_message(self, phone_number: str, value: str) -> None:
            raise NotImplementedError

Steps to Implement a Backend
=============================

1. **Create the Backend Class**

   Implement the `ISmsProvider` interface for the service. This class will handle sending single, bulk, and verification SMS messages.

2. **Handle Dependencies**

   Ensure necessary dependencies (e.g., `twilio`, `sms_ir`) are imported and handled appropriately. The `try-except` block checks for the presence of the required library and raises an error if it is not installed.

3. **Validate Phone Numbers**

   Use the `PhoneNumberValidator` class to validate and format phone numbers to ensure they are in the correct format before sending.

4. **Implement Methods**

   Implement the `send_one_message`, `send_bulk_messages`, and `send_verify_message` methods as required by the `ISmsProvider` interface. These methods handle the actual sending of messages via the respective service.

5. **Add Configuration**

   Update your settings to include the new backend provider with the required API key and line number. This configuration will be used to initialize the backend.

**Create SMS Backend Parameters**

The following table lists the parameters you can use when configuring the SMS backend:

.. list-table::
   :header-rows: 1

   * - Param Name
     - Type
     - Description
   * - ``API_KEY`` (required)
     - String
     - The API key for the SMS service.
   * - ``AUTH_TOKEN`` (Twilio only)
     - String
     - The authentication token for the Twilio service.
   * - ``LINE_NUMBER``
     - String
     - The line number used for sending SMS.

Using the SMS Backend
======================

To use the SMS backend, follow these steps:

.. code-block:: python

    # Import the factory class from the package
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

By following these steps, a new SMS backend can be created and integrated into the Sage SMS package, allowing for seamless SMS sending capabilities through various providers.
