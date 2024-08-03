import logging
import os
from importlib import import_module
from typing import ClassVar, Dict

from sage_sms.backends.base import ConsoleSMSBackend
from sage_sms.design.interfaces.provider import ISmsProvider
from sage_sms.helper.exceptions import (
    SMSBackendError,
    SMSConfigurationError,
    SMSProviderNotFoundError,
    SMSUnexpectedError,
)
from sage_sms.helper.type import ProviderSettings, SMSSettings

logger = logging.getLogger(__name__)


class BackendModuleLoader:
    _cached_backends: ClassVar[Dict[str, type]] = {}
    _provider_classname_map: ClassVar[Dict[str, type]] = {}

    @classmethod
    def discover_backends(cls, base_package: str):
        logger.debug(f"Discovering backends in package: {base_package}")
        base_path = base_package.replace(".", "/")
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_name = file[:-3]  # Strip '.py' extension
                    module = import_module(f"{base_package}.{module_name}")
                    for name, obj in module.__dict__.items():
                        if (
                            isinstance(obj, type)
                            and issubclass(obj, ISmsProvider)
                            and obj is not ISmsProvider
                        ):
                            cls._provider_classname_map[module_name] = obj.__name__
                            logger.debug(
                                f"Found provider: {module_name}.{obj.__name__}"
                            )
                            break

    @staticmethod
    def load_backend_module(provider: ProviderSettings, base_package: str):
        provider_name = provider.get("NAME")
        logger.debug(f"Loading backend module for provider: {provider_name}")

        if not provider_name:
            logger.error("Provider key is missing in settings.")
            raise SMSConfigurationError("Provider key is missing in settings.")

        if provider_name not in BackendModuleLoader._provider_classname_map:
            logger.error(f"Unsupported provider: {provider_name}")
            raise SMSProviderNotFoundError(f"Unsupported provider: {provider_name}")

        if provider_name in BackendModuleLoader._cached_backends:
            logger.debug(f"Using cached backend for provider: {provider_name}")
            return BackendModuleLoader._cached_backends[provider_name]

        class_name = BackendModuleLoader._provider_classname_map[provider_name]
        module = import_module(f"{base_package}.{provider_name}")
        provider_class = getattr(module, class_name)
        BackendModuleLoader._cached_backends[provider_name] = provider_class
        logger.debug(f"Loaded backend module: {provider_name}.{class_name}")
        return provider_class


class SMSBackendFactory:
    def __init__(self, settings: SMSSettings, base_package: str):
        self.settings = settings
        self.base_package = base_package
        try:
            BackendModuleLoader.discover_backends(base_package)
            logger.debug(f"Discovered backends for package: {base_package}")
        except Exception as e:
            logger.exception(f"Unexpected error during backend discovery: {e}")
            raise SMSUnexpectedError(f"Unexpected error during backend discovery: {e}")

    def get_backend(self, *args, **kwargs):
        try:
            if self.settings.get("debug", False):
                logger.debug("Debug mode enabled, using ConsoleSMSBackend")
                return ConsoleSMSBackend

            backend_class = BackendModuleLoader.load_backend_module(
                self.settings.get("provider"), self.base_package
            )
            logger.debug(f"Loaded backend class: {backend_class}")
            return backend_class
        except SMSBackendError as e:
            logger.exception(f"SMSBackendError occurred: {e}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error while getting backend: {e}")
            raise SMSUnexpectedError(f"Unexpected error while getting backend: {e}")
