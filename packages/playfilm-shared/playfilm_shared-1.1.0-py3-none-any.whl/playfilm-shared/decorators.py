import functools
import logging
import traceback
from logging.handlers import SysLogHandler
from typing import Any, Callable


def logging_function(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger = init_logger()
        value = None
        try:
            value = func(*args, **kwargs)
            if value is not None:
                logger.info(f'Logging in {func.__name__} return value {value}')
        except Exception as error:
            logger.error(
                f"Error in {func.__name__} with {error} traceback: {traceback.format_exc()}")
        return value

    def init_logger():
        host = "logs.papertrailapp.com"
        port = 40259
        logger = logging.getLogger("vicEscribano")
        logger.setLevel(logging.DEBUG)
        handler = SysLogHandler(address=(host, port))
        logger.addHandler(handler)
        return logger

    return wrapper
