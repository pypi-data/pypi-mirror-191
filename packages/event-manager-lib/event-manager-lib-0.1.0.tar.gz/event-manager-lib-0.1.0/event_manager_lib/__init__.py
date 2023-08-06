import logging

__version__ = '0.1.0'

def enabled_logger(name: str ="event-manager-library", level: int  = logging.DEBUG, logger_format: str = None):
    """
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all event-manager-library messages to ``stdout``.
    """

    if logger_format is None:
        logger_format =  "%(asctime)s %(name)s [%(levelname)s] %(message)s"
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter(logger_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Set up logging to ``/dev/null`` like a library is supposed to.
# https://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logging.getLogger("event-manager-library").addHandler(NullHandler())