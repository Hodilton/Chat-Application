import logging
import os
from typing import Dict, Union, List
from .._internal.base_logger import LogFormatter
from .._handlers.color_handler import ColorHandler
from .._handlers.rotating_size_handler import RotatingSizeHandler
from .._handlers.time_rotating_handler import TimeRotatingHandler
from .logger_config import LoggerConfig
from .._utils.directory import Directory


class LogManager:
    VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    VALID_HANDLER_TYPES = {"console", "file", "rotate_size", "rotate_time"}

    def __init__(self, config: LoggerConfig):
        self._loggers: Dict[str, logging.Logger] = {}
        self._config = config
        self._initialize_loggers()

    def _initialize_loggers(self):
        for name, cfg in self._config.get_config().items():
            logger = logging.getLogger(name)
            level_str = cfg.get("level", "DEBUG").upper()
            if level_str not in self.VALID_LEVELS:
                raise ValueError(f"Invalid log level '{level_str}' for logger '{name}'")
            logger.setLevel(getattr(logging, level_str))
            logger.propagate = False

            handler = self._create_handler(cfg)
            handler.setFormatter(LogFormatter.get_formatter())
            logger.addHandler(handler)

            self._loggers[name] = logger

    def _create_handler(self, cfg: Dict) -> logging.Handler:
        typ = cfg["type"]
        if typ not in self.VALID_HANDLER_TYPES:
            raise ValueError(f"Unknown logger type: '{typ}'. Valid types: {self.VALID_HANDLER_TYPES}")

        if typ == "console":
            use_color_console = cfg.get("use_color", True)
            return ColorHandler() if use_color_console else logging.StreamHandler()
        else:
            path = os.path.join(self._config.log_dir, cfg["path"])
            Directory.ensure_dir_for_file(path)
            if typ == "file":
                return logging.FileHandler(path, encoding="utf-8")
            elif typ == "rotate_size":
                return RotatingSizeHandler(path,
                                           cfg.get("max_bytes", 10240),
                                           cfg.get("backup_count", 3))
            elif typ == "rotate_time":
                return TimeRotatingHandler(path,
                                           cfg.get("when", "midnight"),
                                           cfg.get("interval", 1),
                                           cfg.get("backup_count", 7))

    def log(self, targets: Union[str, List[str]], message: str, level: str = "INFO"):
        level = level.upper()
        if level not in self.VALID_LEVELS:
            raise ValueError(f"Invalid log level '{level}'. Valid levels: {self.VALID_LEVELS}")

        if isinstance(targets, str):
            targets = [targets]

        for name in targets:
            logger = self._loggers.get(name)
            if logger:
                getattr(logger, level.lower())(message)
            else:
                logging.warning(f"Logger '{name}' not found. Message not logged: {message}")

    def log_all(self, message: str, level: str = "INFO"):
        self.log(list(self._loggers.keys()), message, level)
