import logging

logger = logging.getLogger("my_module")  # Get a logger named 'my_module'
logger.setLevel(logging.DEBUG)            # Set minimum level to DEBUG

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("An error occurred")
logger.critical("Critical failure!")
