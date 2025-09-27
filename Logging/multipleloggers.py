import logging

# Create a logger
logger = logging.getLogger('my_logger')

# Set level for this logger
logger.setLevel(logging.DEBUG)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)

# Use the logger
logger.debug("This is a debug message")
logger.info("Info message from my_logger")
