Overview
========

The Sage SMS package is designed to facilitate the sending of SMS messages through various providers. This package provides a flexible and extensible framework for integrating multiple SMS backends, validating phone numbers, and handling SMS-related errors.

Key Features
============

- **Modular Design**: The package is organized into modules for different functionalities, including backend management, phone number validation, and exception handling.
- **Backend Discovery and Loading**: SMS backends are dynamically discovered and loaded based on the provided configuration.
- **Phone Number Validation**: Phone numbers are validated and formatted using the `phonenumbers` library to ensure compliance with international standards.
- **Exception Handling**: Custom exceptions are defined for various error scenarios, providing clear and specific error messages.

Creating a Backend
==================

To create a new SMS backend, follow these steps:

1. **Implement the ISmsProvider Interface**: Create a class that implements the methods defined in the `ISmsProvider` interface.
2. **Add Backend Module**: Add the new backend module to the appropriate package directory.
3. **Update Configuration**: Update the configuration settings to include the new backend provider.

For detailed instructions, refer to the section :ref:`Creating an SMS Backend <creating-backends>`.

Using a Backend
===============

To use an SMS backend, import the necessary modules and configure the settings for the desired SMS provider. The following steps are involved:

1. **Setup Logging**: Configures the logging settings for the application.
2. **Initialize Factory**: Create an instance of `SMSBackendFactory` with the provided settings and base package.
3. **Get Backend**: Retrieve the backend class based on the configuration.
4. **Send Messages**: Use the backend instance to send single, bulk, and verification SMS messages.

Conclusion
==========

The Sage SMS package offers a robust and flexible solution for sending SMS messages through various providers. Its modular design, comprehensive validation, and detailed error handling make it a reliable choice for integrating SMS functionality into applications.
