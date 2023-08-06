import logging


def getLoggerConfig(level: str = None, handlers: list = None,
            propagate: bool = None, filters: list = None) -> dict:
    """Create and return a logger config.

    Parameters
    ----------
    level : str, optional
        The level of the logger, by default None
    handlers : list, optional
        A list of ids of the handlers for this logger by default None
    propagate : bool, optional
        The propagation setting of the logger, by default None
    filters : list, optional
        A list of ids of the filters for this logger, by default None

    Returns
    -------
    dict
        logger config.
    """
    config = {}
    if level is not None:
        config["level"] = level
    if handlers is not None:
        config["handlers"] = handlers
    if propagate is not None:
        config["propagate"] = propagate
    if filters is not None:
        config["filters"] = filters
    return config


class Logger(logging.Logger):
    pass
