"""
SMS Backend Module

This module provides abstract and concrete classes for SMS backends.
The abstract class `BaseSMSBackend` serves as a template for implementing
other SMS backends. The concrete class `ConsoleSMSBackend` is an implementation
that writes SMS messages to the console (stdout).

Classes:
    BaseSMSBackend: Abstract base class for SMS backends.
    ConsoleSMSBackend: Implementation of an SMS backend
    that writes messages to the console.

Usage:
    # Using ConsoleSMSBackend
    backend = ConsoleSMSBackend()
    backend.send_one_message("1234567890", "Hello, World!", "Your line number")

Exceptions:
    None
"""

import sys

from ..design.interfaces.provider import ISmsProviderFactory


class BaseSMSBackend:
    """
    BaseSMSBackend Class (Abstract)

    This class serves as an abstract base class for SMS backends.

    Attributes:
        sms_provider (ISmsProviderFactory): A factory object
        that creates an SMS provider.

    Methods:
        None
    """

    def __init__(self, factory: ISmsProviderFactory = None):
        """
        Initialize a new BaseSMSBackend instance.

        Args:
            factory (ISmsProviderFactory, optional): Factory to create an SMS provider.
        """
        self.sms_provider = factory.create_sms_provider() if factory else None


class ConsoleSMSBackend(BaseSMSBackend):
    """
    ConsoleSMSBackend Class

    This class is a concrete implementation of BaseSMSBackend that writes SMS messages
    to the console (stdout).

    Attributes:
        stream (file-like object): The output stream to write messages.
    """

    def __init__(self, factory: ISmsProviderFactory = None, stream=None):
        """
        Initialize a new ConsoleSMSBackend instance.

        Args:
            factory (ISmsProviderFactory, optional): Factory to create an SMS provider.
            stream (file-like object, optional): The output stream to write messages.
        """
        super().__init__(factory)
        self.stream = stream or sys.stdout

    def _write_message(self, message: str):
        """
        Write a message to the output stream.

        Args:
            message (str): The message to write.
        """
        self.stream.write(f"\n{message}")
        self.stream.write("-" * 79)
        self.stream.write("\n")

    def send_one_message(
        self, phone_number: str, message: str, line_number: str | None = None
    ):
        """
        Send a single message.

        Args:
            phone_number (str): The recipient's phone number.
            message (str): The message content.
            line_number (str): The sender's line number.
        """
        msg = (
            f"Recipient: {phone_number}\nMessage: {message}\nLine Number: {line_number}"
        )
        self._write_message(msg)

    def send_bulk_messages(
        self, phone_numbers: list[str], message: str, line_number: str | None = None
    ):
        """
        Send bulk messages.

        Args:
            phone_numbers (list[str]): List of recipient's phone numbers.
            message (str): The message content.
            line_number (str): The sender's line number.
        """
        for phone_number in phone_numbers:
            self.send_one_message(phone_number, message, line_number)

    def send_verify_message(self, phone_number: str, value: str):
        """
        Send a verification message.

        Args:
            phone_number (str): The recipient's phone number.
            value (str): The verification code or value.
        """
        msg = f"Recipient: {phone_number}\nVerification Code: {value}"
        self._write_message(msg)
