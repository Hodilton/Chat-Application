import json
from typing import Dict, Optional, Any


class LoggerConfig:
    REQUIRED_KEYS = {"type"}

    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        config_path: Optional[str] = None,
        log_dir: str = "logs"
    ):
        self.log_dir = log_dir
        if config_path:
            self._config = self._load_config_from_file(config_path)
        else:
            self._config = config or {}

        self._validate_config()

    @staticmethod
    def _load_config_from_file(path: str) -> Dict[str, Any]:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _validate_config(self):
        def _validate_config(self):
            for logger_name, cfg in self._config.items():
                if not isinstance(cfg, dict):
                    raise TypeError(f"Config for logger '{logger_name}' must be a dict")
                if "type" not in cfg:
                    raise ValueError(f"Logger '{logger_name}' config missing required key: 'type'")

                typ = cfg["type"]
                if typ not in {"console", "file", "rotate_size", "rotate_time"}:
                    raise ValueError(f"Logger '{logger_name}' has invalid type '{typ}'")

                if typ != "console" and "path" not in cfg:
                    raise ValueError(f"Logger '{logger_name}' of type '{typ}' requires 'path' key")

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def add_loggers(self, new_cfg: Dict[str, Any]) -> None:
        for key, val in new_cfg.items():
            if key in self._config and isinstance(self._config[key], dict) and isinstance(val, dict):
                self._config[key].update(val)
            else:
                self._config[key] = val
