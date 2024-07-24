import sys

from ..design.interfaces.provider import ISmsProvider


class BaseSMSBackend:
    def __init__(self, settings: dict):
        self.settings = settings


class ConsoleSMSBackend(BaseSMSBackend):
    def __init__(self, settings: dict, stream=None):
        super().__init__(settings)
        self.stream = stream or sys.stdout

    def _write_message(self, message: str):
        self.stream.write(f"\n{message}")
        self.stream.write("-" * 79)
        self.stream.write("\n")

    def send_one_message(self, phone_number: str, message: str, line_number: str | None = None):
        msg = f"Recipient: {phone_number}\nMessage: {message}\nLine Number: {line_number}"
        self._write_message(msg)

    def send_bulk_messages(self, phone_numbers: list[str], message: str, line_number: str | None = None):
        for phone_number in phone_numbers:
            self.send_one_message(phone_number, message, line_number)

    def send_verify_message(self, phone_number: str, value: str):
        msg = f"Recipient: {phone_number}\nVerification Code: {value}"
        self._write_message(msg)
