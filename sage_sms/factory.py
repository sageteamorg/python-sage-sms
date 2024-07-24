"""
SMS Backend Loading and Factory Module

This module contains classes responsible for loading the appropriate SMS
backend modules and creating instances of those backends.

Classes:
    - BackendModuleLoader: Class for loading SMS backend modules by provider name.
    - SMSBackendFactory: Factory class for creating instances of SMS backends.

Exceptions:
    - ImportError: Raised when the required package for a provider is not installed.

Usage:
    Use `BackendModuleLoader.load_backend_module` to load a backend module.
    Use `SMSBackendFactory.get_backend` to get an instance of the appropriate backend.

Example:
    >>> backend = SMSBackendFactory.get_backend(True, False, 'sms_ir')
"""
from importlib import import_module
from typing import ClassVar, Dict

from .backend.base import ConsoleSMSBackend


class BackendModuleLoader:
    """
    BackendModuleLoader Class

    Responsible for dynamically loading SMS backend modules given a provider name.

    Attributes:
        _cached_backends (dict): A dictionary to cache loaded backend classes.
        _provider_classname_map (dict): A mapping from provider name
        to backend class name.
    """

    _cached_backends: ClassVar[Dict[str, str]] = {}
    _provider_classname_map: ClassVar[Dict[str, str]] = {
        "sms_ir": "SmsIr",
        "kavenegar": "Kavenegar",
    }

    @staticmethod
    def load_backend_module(provider: dict):
        """
        Load a backend module given the provider name.

        Args:
            provider (dict): The name of the SMS provider.

        Returns:
            class: The SMS backend class corresponding to the provider.

        Raises:
            ImportError: Raised when the required package
            for the provider is not installed.
        """
        provider_name = provider.get("NAME")

        if not provider_name:
            raise ValueError("Provider name is missing in settings.")

        if provider_name not in BackendModuleLoader._provider_classname_map:
            raise ValueError(f"Unsupported provider: {provider_name}")

        if provider_name in BackendModuleLoader._cached_backends:
            return BackendModuleLoader._cached_backends[provider_name]

        class_name = BackendModuleLoader._provider_classname_map.get(
            provider_name, f"{provider_name.capitalize()}Backend"
        )

        try:
            module = import_module(f"account.communication.backend.{provider_name}")
            backend_class = getattr(module, class_name)
            BackendModuleLoader._cached_backends[provider_name] = backend_class
            return backend_class
        except ImportError as err:
            raise ImportError(
                f"You must install the package for {provider_name}."
            ) from err


class SMSBackendFactory:
    """
    SMSBackendFactory Class

    Factory class for creating instances of various SMS backends.

    Methods:
        - get_backend: Get an instance of the appropriate SMS backend.
    """

    @staticmethod
    def get_backend(settings: dict, *args, **kwargs):
        """
        Get an instance of the appropriate SMS backend
        based on settings and provider name.

        Args:
            is_sms_debug_enabled (bool): Flag to enable debug mode.
            provider (str): The name of the SMS provider.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: An instance of the appropriate SMS backend class.
        """

        if (debug := settings.get("debug")) is not None:
            if debug:
                return ConsoleSMSBackend()
        else:
            return ConsoleSMSBackend()

        backend_class = BackendModuleLoader.load_backend_module(
            settings.get("provider")
        )

        # Initialize the backend class with any additional arguments
        # or keyword arguments
        return backend_class(*args, **kwargs)
