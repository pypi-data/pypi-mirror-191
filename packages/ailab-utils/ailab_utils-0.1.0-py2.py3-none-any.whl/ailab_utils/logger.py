import logging
from typing import Optional


class CustomLoggerAdapter(logging.LoggerAdapter):
    def __init__(
        self, name: str, kwargs: dict, formatter: Optional[logging.Formatter] = None
    ) -> None:
        """
        CustomLoggerAdapter is a subclass of logging.LoggerAdapter that provides a
        custom logging implementation with support for adding a "service" field to
        the log message.

        This adapter is initialized with a logger name and a set of keyword arguments.
        A formatter can also be specified, which will be applied to the logger's
        handler. If no formatter is specified, a default formatter will be used.

        The process() method is used to process a log message, adding a "service"
        field to the log message if one is specified in the keyword arguments.

        Attributes:
            logger (logging.Logger): A logging.Logger object that is used for
                logging messages.
            kwargs (dict): A dictionary of keyword arguments to be passed to the
                logging.LoggerAdapter.
            formatter (Optional[logging.Formatter]): A logging.Formatter object
                that is used to format log messages.
        """
        self.logger = logging.getLogger(name)

        handler = logging.StreamHandler()
        if formatter is None:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(module)s (%(filename)s:%(lineno)d): %(message)s"
            )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False
        super().__init__(self.logger, kwargs)

    def process(self, msg, kwargs):
        """
        Process a log message, adding a "service" field to the log message if
        one is specified in the keyword arguments.

        Args:
            msg (str): The log message.
            kwargs (dict): A dictionary of keyword arguments to be passed to the
                logging.Logger.

        Returns:
            tuple: A tuple containing the processed log message and the keyword
                arguments.
        """
        service = kwargs.pop("service", self.extra.get("service"))
        log = "{service} - {msg}".format(
            service=service,
            msg=msg,
        )
        return log, kwargs
