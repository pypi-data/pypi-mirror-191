import logging


def getHandlerConfig(className: str, level: str = None, formatter: str = None,
            filters: list = None, **kwargs) -> dict:
    """Create and return a handler config.

    Parameters
    ----------
    className : str
        This is the fully qualified name of the handler class.
    level : str, optional
        The level of the handler, by default None
    formatter : str, optional
        The id of the formatter for this handler, by default None
    filters : list, optional
        A list of ids of the filters for this handler, by default None

    Returns
    -------
    dict
        handler config.
    """
    config = { "class": className }
    if level is not None:
        config["level"] = level
    if formatter is not None:
        config["formatter"] = formatter
    if filters is not None:
        config["filters"] = filters
    config.update(kwargs)
    return config


def getConsleHandlerConfig(level: str = None, formatter: str = None,
            stream: str = "ext://sys.stdout") -> dict:
    """Create and return a consle handler config.

    Parameters
    ----------
    level : str, optional
        The level of the handler, by default None
    formatter : str, optional
        The id of the formatter for this handler, by default None
    stream : str, optional
        The stream that the handler should use, by default "ext://sys.stdout"

    Returns
    -------
    dict
        consle handler config.
    """
    return getHandlerConfig(
        f"{ConsoleHandler.__module__}.{ConsoleHandler.__name__}",
        level,
        formatter,
        stream = stream)


class ConsoleHandler(logging.StreamHandler):
    pass
