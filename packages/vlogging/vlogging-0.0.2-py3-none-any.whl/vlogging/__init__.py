import logging
import logging.config
from typing import Any

from vlogging import (
    formatters,
    handlers,
    loggers,
)
from vlogging.loggers import Logger

from logging import (
    CRITICAL,
    FATAL,
    ERROR,
    WARNING,
    WARN,
    INFO,
    DEBUG,
    NOTSET,
)

__version__ = "0.0.2"

__all__ = ["Logger"]

class Config(object):

    DEFAUT_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "defaut_format": formatters.getFormatConfig(formatters.SIMPLE_FORMAT),
        },
        "filters": {},
        "handlers": {
            "defaut_handler": handlers.getConsleHandlerConfig("DEBUG", "defaut_format"),
        },
        "loggers": {
            "vlogging": loggers.getLoggerConfig("DEBUG", ["defaut_handler"]),
        },
    }

    def __init__(self):
        """Initializes the instance."""
        self.config = self.DEFAUT_CONFIG.copy()

    def configure(self, config: dict=None) -> None:
        """Configure logger settings.

        Parameters
        ----------
        config : dict, optional
            config, by default None
        """
        if config is not None:
            self.config["formatters"] = self.configureFormatters(config)
            self.config["filters"] = self.configureFilters(config)
            self.config["handlers"] = self.configureHandlers(config)
            self.config["loggers"] = self.configureLoggers(config)
        logging.config.dictConfig(self.config)

    def configureFormatters(self, config: dict) -> dict:
        """Configure formatter settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            format config.
        """
        return self.configureItems(config, "formatters", "defaut_format")

    def configureFilters(self, config: dict) -> dict:
        """Configure filter settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            filter config.
        """
        return self.configureItems(config, "filters", None)

    def configureHandlers(self, config: dict) -> dict:
        """Configure handler settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            handler config.
        """
        return self.configureItems(config, "handlers", "defaut_handler")

    def configureLoggers(self, config: dict) -> dict:
        """Configure logger settings.

        Parameters
        ----------
        config : dict
            config

        Returns
        -------
        dict
            logger config.
        """
        return self.configureItems(config, "loggers", "vlogging")

    def configureItems(self, config: dict, key: str, defaut: str) -> dict:
        """Configure logger item settings.

        Parameters
        ----------
        config : dict
            config
        key : str
            config key
        defaut : str
            defaut key

        Returns
        -------
        dict
            logger item config.
        """
        result = self.configureDefautConfig(key, defaut)
        if config is None:
            cfg = {}
        else:
            cfg = config.get(key, {})

        if defaut is not None and cfg.get(defaut, None) is None:
            cfg.pop(defaut, None)

        for name in cfg:
            result[name] = cfg[name]
        return result

    def configureDefautConfig(self, key: str, defaut: str) -> dict:
        """Returns the specified default settings.

        Parameters
        ----------
        key : str
            config key
        defaut : str
            defaut key

        Returns
        -------
        dict
            defaut config.
        """
        result = {}
        if defaut is not None:
            result[defaut] = self.DEFAUT_CONFIG[key][defaut].copy()
        return result

    def prepare(self, name: str) -> None:
        """Prepare a logger with the given logger name.

        Parameters
        ----------
        name : str
            logger name
        """
        if name is None:
            return
        loggers = self.config.get("loggers")
        if name not in loggers.keys():
            loggers[name] = loggers.get("vlogging").copy()
            self.configure()


def getLogger(name: str=None, config: dict=None) -> Logger:
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.

    Parameters
    ----------
    name : str, optional
        logger name, by default None
    config : dict, optional
        Configure logging using a dictionary, by default None

    Returns
    -------
    Logger
        logger
    """
    if config is not None:
        _config.configure(config)
    if name is not None:
        _config.prepare(name)
    return logging.getLogger(name)


def critical(msg: Any, *args, **kwargs):
    """Log a message with severity 'CRITICAL' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.critical(msg, *args, **kwargs)


def fatal(msg: Any, *args, **kwargs):
    """Don't use this function, use critical() instead.

    Parameters
    ----------
    msg : Any
        log message
    """
    critical(msg, *args, **kwargs)


def error(msg: Any, *args, **kwargs):
    """Log a message with severity 'ERROR' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.error(msg, *args, **kwargs)


def exception(msg: Any, *args, exc_info=True, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger, with exception
    information.

    Parameters
    ----------
    msg : Any
        log message
    exc_info : bool, optional
        exception information, by default True
    """
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg: Any, *args, **kwargs):
    """Log a message with severity 'WARNING' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.warning(msg, *args, **kwargs)


def info(msg: Any, *args, **kwargs):
    """Log a message with severity 'INFO' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.info(msg, *args, **kwargs)


def debug(msg: Any, *args, **kwargs):
    """Log a message with severity 'DEBUG' on the root logger.

    Parameters
    ----------
    msg : Any
        log message
    """
    _logger.debug(msg, *args, **kwargs)


def log(level: int, msg: Any, *args, **kwargs):
    """Log 'msg % args' with the integer severity 'level' on the logger.

    Parameters
    ----------
    level : int
        log level
    msg : Any
        log message
    """
    _logger.log(level, msg, *args, **kwargs)


logging.setLoggerClass(Logger)
_config: Config = Config()
_config.configure()
_logger = getLogger(__name__)
