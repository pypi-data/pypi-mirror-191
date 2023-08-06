import logging
from datetime import datetime

SIMPLE_FORMAT = "%(asctime)s %(levelname)-8s %(message)s"
BASIC_FORMAT = "%(asctime)s %(levelname)-8s %(filename)s:%(lineno)d: %(message)s"
DATE_FMT_MICROSECONDS = "%Y-%m-%d %H:%M:%S.%f"

def getFormatConfig(format: str, datefmt: str = None, style: str = "%",
            className: str = "vlogging.formatters.Formatter",  **kwargs) -> dict:
    """Create and return a format config.

    Parameters
    ----------
    format : str
        The format string to use.
    datefmt : str, optional
        The date format string to use, by default None
    style : str, optional
        The style parameter to use, by default "%"
    className : str, optional
        This is the fully qualified name of the formatter class, by default "vlogging.formatters.Formatter"

    Returns
    -------
    dict
        format config.
    """
    config = {
        "class": className,
        "format": format,
        "style": style,
    }
    if datefmt is not None:
        config["datefmt"] = datefmt
    config.update(kwargs)
    return config


def getMicrosecondsFormatConfig(format: str = BASIC_FORMAT, style: str = "%") -> dict:
    """Create and return a microseconds date format config.

    Parameters
    ----------
    format : str, optional
        The format string to use, by default BASIC_FORMAT
    style : str, optional
        The style parameter to use, by default "%"

    Returns
    -------
    dict
        microseconds date format config.
    """
    return getFormatConfig(format, DATE_FMT_MICROSECONDS, style)


class Formatter(logging.Formatter):
    """
    Formatter instances are used to convert a LogRecord to text.

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(process)d         Process ID (if available)
    %(processName)s     Process name (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """


    def formatTime(self, record: logging.LogRecord, datefmt: str=None) -> str:
        """
        Return the creation time of the specified LogRecord as formatted text.

        Parameters
        ----------
        record : logging.LogRecord
            log record
        datefmt : str, optional
            datetime format, by default None

        Returns
        -------
        str
            formatted text
        """
        dt = datetime.fromtimestamp(record.created)
        if datefmt is None:
            time = dt.isoformat(sep=" ", timespec="milliseconds")
        else:
            time = dt.strftime(datefmt)
        return time
