import os
from importlib import import_module
from typing import ClassVar, Dict

from .backends.base import ConsoleSMSBackend
from .design.interfaces.provider import ISmsProvider


class BackendModuleLoader:
    _cached_backends: ClassVar[Dict[str, type]] = {}
    _provider_classname_map: ClassVar[Dict[str, type]] = {}

    @classmethod
    def discover_backends(cls, base_package: str):
        base_path = base_package.replace('.', '/')
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith('.py') and file != '__init__.py':
                    module_name = file[:-3]  # Strip '.py' extension
                    module = import_module(f"{base_package}.{module_name}")
                    for name, obj in module.__dict__.items():
                        if isinstance(obj, type) and issubclass(obj, ISmsProvider) and obj is not ISmsProvider:
                            cls._provider_classname_map[module_name] = obj.__name__
                            break

    @staticmethod
    def load_backend_module(provider: dict, base_package: str):
        provider_name = provider.get("NAME")

        if not provider_name:
            raise ValueError("Provider key is missing in settings.")

        if provider_name not in BackendModuleLoader._provider_classname_map:
            raise ValueError(f"Unsupported provider: {provider_name}")

        if provider_name in BackendModuleLoader._cached_backends:
            return BackendModuleLoader._cached_backends[provider_name]

        class_name = BackendModuleLoader._provider_classname_map[provider_name]
        module = import_module(f"{base_package}.{provider_name}")
        provider_class = getattr(module, class_name)
        BackendModuleLoader._cached_backends[provider_name] = provider_class
        return provider_class


class SMSBackendFactory:

    def __init__(self, settings: dict, base_package: str):
        BackendModuleLoader.discover_backends(base_package)
        self.settings = settings
        self.base_package = base_package

    def get_backend(self, *args, **kwargs):
        if self.settings.get("debug", False):
            return ConsoleSMSBackend

        backend_class = BackendModuleLoader.load_backend_module(self.settings.get("provider"), self.base_package)
        return backend_class
