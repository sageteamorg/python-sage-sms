"""
SMS Provider Interface Module

This module defines abstract base classes (ABCs) for creating SMS providers.
These ABCs serve as interfaces that must be implemented by concrete classes
for sending SMS messages in various manners (single, bulk, verification).

Classes:
    - ISmsProviderFactory: Interface for factories creating SMS providers.
    - ISmsProvider: Interface for SMS providers.

Usage:
    Implement these interfaces when creating new classes for SMS providers.

Exceptions:
    NotImplementedError: Raised when an implemented method does not
    meet the requirements of the interface.
"""

from abc import ABC, abstractmethod


class ISmsProviderFactory(ABC):
    """
    ISmsProviderFactory Interface

    This interface serves as an abstract base class for factories that
    create SMS providers.

    Methods:
        - create_sms_provider: Abstract method to create an SMS provider.
    """

    @abstractmethod
    def create_sms_provider(self) -> "ISmsProvider":
        """
        Create an instance of an SMS provider.

        Returns:
            ISmsProvider: An instance that conforms to the ISmsProvider interface.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError


class ISmsProvider(ABC):
    """
    ISmsProvider Interface

    This interface serves as an abstract base class for SMS providers.

    Methods:
        - send_one_message: Send a single SMS message.
        - send_bulk_messages: Send bulk SMS messages.
        - send_verify_message: Send a verification SMS message.
    """

    @abstractmethod
    def send_one_message(self, phone_number: str, message: str, linenumber) -> None:
        """
        Send a single SMS message.

        Args:
            phone_number (str): The recipient's phone number.
            message (str): The content of the message.
            linenumber: The sender's line number.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def send_bulk_messages(
        self, phone_numbers: list[str], message: str, linenumber
    ) -> None:
        """
        Send bulk SMS messages.

        Args:
            phone_numbers (list[str]): List of recipient phone numbers.
            message (str): The content of the messages.
            linenumber: The sender's line number.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError

    @abstractmethod
    def send_verify_message(self, phone_number: str, value: str) -> None:
        """
        Send a verification SMS message.

        Args:
            phone_number (str): The recipient's phone number.
            value (str): The verification value or code.

        Raises:
            NotImplementedError: This method must be implemented by a subclass.
        """
        raise NotImplementedError
