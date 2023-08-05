# -*- coding: utf-8 -*-
# pylint: disable=C0114

import logging
from typing import Any, List, NoReturn

LOGGER = logging.getLogger(__name__)


class ObjectConfigBase:
    _config: dict

    def __init__(self, **kwargs):
        self._config = {k: v for k, v in kwargs.items() if v is not None}
        self.setup()
        self.validate()

    def setup(self):
        pass

    def validate(self):
        pass

    @property
    def config(self) -> dict:
        return self._config

    def check_obj_isinstance(self, tp_obj: type, obj, name):
        if not isinstance(obj, tp_obj):
            raise TypeError(
                f'{name} is required, valid instance of {tp_obj.__module__}.{tp_obj.__name__}'
            )

    def get_config(self, *keys):
        value = None
        for key in keys:
            if key in self.config:
                value = value or self.config.get(key)
            if value is None:
                continue
            if isinstance(value, str) and len(value) > 0:
                break
        return value

    def get_str_config(self, *keys) -> str:
        value = self.get_config(self, *keys)
        if isinstance(value, bool):
            value = 'true' if value else 'false'
        return str(value) if value is not None else value

class ObjectConfigContainerBase(ObjectConfigBase):
    _container: dict
    _containers: List["ObjectConfigContainerBase"]

    def __init__(self, container: "ObjectConfigContainerBase" = None, **kwargs) -> NoReturn:
        self._container = None
        self._containers: List["ObjectConfigContainerBase"] = []
        super().__init__(**kwargs)
        if self._container is not None:
            self._container = container.container
            self._containers.append(container)

    @property
    def container(self) -> dict:
        return self._container

    @property
    def containers(self) -> List["ObjectConfigContainerBase"]:
        return self._containers

    def _get_in_container_fnc(self, key: str, containers: List["ObjectConfigContainerBase"] = None, default: Any = None) -> Any:
        keys = [
            f"get_{key}".replace(".", "_"),
            f"create_{key}".replace(".", "_"),
            f"factory_{key}".replace(".", "_")
        ]
        for container in ([] if containers is None else containers):
            for fnc_name in keys:
                if hasattr(container, fnc_name):
                    try:
                        fnc = getattr(container, fnc_name)
                        if callable(fnc):
                            return self.set(key, fnc())
                    except Exception:
                        continue
        for container in self.containers:
            if hasattr(container, "get"):
                item = container.get(key)
                if item is not None:
                    return self.set(key, item)
        return default

    def get(self, key: str, default: Any = None) -> Any:
        if hasattr(self, key):
            return getattr(self, key)
        if key in self.container:
            return self.container.get(key, default)
        if key in self.config:
            return self.config.get(key, default)
        containers = [self]
        if self.container is not None:
            containers.append(self.container)
        return self._get_in_container_fnc(key, containers, default)

    def set(self, key: str, value: Any) -> Any:
        try:
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception()
        except Exception:
            self.container[key] = value
        return value
