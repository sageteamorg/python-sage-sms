import sys


class BaseSMSBackend:
    """
    Base class for SMS backend implementations.

    Args:
        settings (dict): The settings for the SMS backend.
    """

    def __init__(self, settings: dict):
        self.settings = settings


class ConsoleSMSBackend(BaseSMSBackend):
    """
    SMS backend class for sending messages to the console.

    Args:
        settings (dict): The settings for the SMS backend.
        stream: The output stream where messages will be written (default is sys.stdout).
    """

    def __init__(self, settings: dict, stream=None):
        super().__init__(settings)
        self.stream = stream or sys.stdout

    def _write_message(self, message: str):
        """
        Write a message to the output stream.

        Args:
            message (str): The message to be written.
        """
        self.stream.write(f"\n{message}")
        self.stream.write("-" * 79)
        self.stream.write("\n")

    def send_one_message(
        self, phone_number: str, message: str, line_number: str | None = None
    ):
        """
        Send a single SMS message to the console.

        Args:
            phone_number (str): The recipient's phone number.
            message (str): The SMS message to be sent.
            line_number (str, optional): The line number used for sending the message.
        """
        msg = (
            f"Recipient: {phone_number}\nMessage: {message}\nLine Number: {line_number}"
        )
        self._write_message(msg)

    def send_bulk_messages(
        self, phone_numbers: list[str], message: str, line_number: str | None = None
    ):
        """
        Send multiple SMS messages to the console.

        Args:
            phone_numbers (list[str]): A list of recipient phone numbers.
            message (str): The SMS message to be sent.
            line_number (str, optional): The line number used for sending the message.
        """
        for phone_number in phone_numbers:
            self.send_one_message(phone_number, message, line_number)

    def send_verify_message(self, phone_number: str, value: str):
        """
        Send a verification code to the console.

        Args:
            phone_number (str): The recipient's phone number.
            value (str): The verification code to be sent.
        """
        msg = f"Recipient: {phone_number}\nVerification Code: {value}"
        self._write_message(msg)
