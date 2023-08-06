import logging
from typing import Optional


class CustomLoggerAdapter(logging.LoggerAdapter):
    def __init__(
        self,
        name: str,
        kwargs: Optional[dict] = None,
        level: str = "DEBUG",
        formatter: Optional[logging.Formatter] = None,
    ) -> None:
        self.formatter = None
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
        if kwargs is None:
            kwargs = {}
        logging.basicConfig(level=level.upper())
        self.logger = logging.getLogger(name)

        self.default_handler = logging.StreamHandler()
        if self.formatter is None:
            self.formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(module)s %(message)s"
            )

        self.default_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.default_handler)
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
        if service is None or service == "":
            return msg, kwargs
        log = "{service} - {msg}".format(
            service=service,
            msg=msg,
        )
        return log, kwargs

    def debug(self, msg, *args, **kwargs):
        DEBUG = 10
        """
        Delegate a debug call to the underlying logger.
        """
        self.logger.removeHandler(self.logger.handlers[0])
        debug_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s %(module)s (%(filename)s:%(lineno)d): %(message)s"
        )
        debug_handler = logging.StreamHandler()
        debug_handler.setFormatter(debug_formatter)
        self.logger.addHandler(debug_handler)
        self.log(DEBUG, msg, *args, **kwargs)
        self.logger.propagate = False
        self.logger.removeHandler(debug_handler)
        self.logger.addHandler(self.default_handler)
