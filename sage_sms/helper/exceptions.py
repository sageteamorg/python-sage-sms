from typing import Optional


class SMSBackendError(Exception):
    """Base class for all SMS backend exceptions."""

    status_code: int = 500
    default_detail: str = "A server error occurred."
    default_code: str = "error"

    def __init__(
        self,
        detail: Optional[str] = None,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
    ):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if status_code is None:
            status_code = self.status_code
        self.detail: str = detail
        self.code: str = code
        self.status_code: int = status_code

    def __str__(self) -> str:
        return f"{self.detail} (Code: {self.code}, Status Code: {self.status_code})"


# Configuration and connection errors
class SMSConfigurationError(SMSBackendError):
    """Exception raised for configuration errors."""

    status_code = 400
    default_detail = "Invalid SMS configuration."
    default_code = "configuration_error"


class SMSConnectionError(SMSBackendError):
    """Exception raised for connection errors."""

    status_code = 502
    default_detail = "Failed to connect to SMS server."
    default_code = "connection_error"


class SMSAuthenticationError(SMSBackendError):
    status_code = 401
    default_detail = "Failed to authenticate with SMS server."
    default_code = "authentication_error"


class SMSProviderError(SMSBackendError):
    status_code = 500
    default_detail = "An SMS provider error occurred."
    default_code = "provider_error"


class SMSProviderNotFoundError(SMSProviderError):
    status_code = 404
    default_detail = "SMS provider not found."
    default_code = "provider_not_found_error"


class SMSProviderExistsError(SMSProviderError):
    status_code = 409
    default_detail = "SMS provider already exists."
    default_code = "provider_exists_error"


class SMSProviderOperationError(SMSProviderError):
    status_code = 500
    default_detail = "Failed to perform provider operation."
    default_code = "provider_operation_error"


# Message-related errors
class SMSMessageError(SMSBackendError):
    status_code = 500
    default_detail = "An SMS message error occurred."
    default_code = "message_error"


class SMSMessageSendError(SMSMessageError):
    status_code = 500
    default_detail = "Failed to send SMS message."
    default_code = "message_send_error"


class SMSMessageFormatError(SMSMessageError):
    status_code = 400
    default_detail = "SMS message format is invalid."
    default_code = "message_format_error"


# Unexpected error
class SMSUnexpectedError(SMSBackendError):
    status_code = 500
    default_detail = "An unexpected error occurred with the SMS service."
    default_code = "unexpected_error"
