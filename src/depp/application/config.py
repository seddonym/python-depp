from typing import Dict, Any


class Settings:
    def __init__(self):
        self._config = {}

    def configure(self, **config_dict: Dict[str, Any]):
        self._config.update(config_dict)

    def __getattr__(self, name):
        if name[:2] != '__':
            return self._config[name]
        return super().__getattr__(name)


settings = Settings()