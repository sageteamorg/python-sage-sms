from .design.interfaces.provider import ISmsProvider


class SmsService:
    def __init__(self, provider: ISmsProvider):
        self._provider = provider

    def set_provider(self, provider: ISmsProvider):
        self._provider = provider

    def send_one_message(self, phone_number: str, message: str, linenumber=None) -> None:
        self._provider.send_one_message(phone_number, message, linenumber)

    def send_bulk_messages(self, phone_numbers: list[str], message: str, linenumber=None) -> None:
        self._provider.send_bulk_messages(phone_numbers, message, linenumber)

    def send_verify_message(self, phone_number: str, value: str):
        self._provider.send_verify_message(phone_number, value)
