from typing import Optional, TypedDict


class ProviderSettings(TypedDict):
    NAME: str
    API_KEY: Optional[str]
    LINE_NUMBER: Optional[str]


class SMSSettings(TypedDict):
    provider: ProviderSettings
    debug: bool
