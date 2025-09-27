import logging

"""
Format code	Description
%(asctime)s	Timestamp of the log message
%(levelname)s	Log level (DEBUG, INFO, etc.)
%(message)s	The log message itself
%(filename)s	Filename where the log was made
%(lineno)d	Line number of the log call
%(funcName)s	Function name where log called
"""


"""logging.basicConfig(
    filename='app.log',        # File to write logs to
    level=logging.DEBUG,       # Minimum level of logs to capture
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format of each log entry
)"""

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s'
)

def my_function():
    logging.info("Inside my_function")

my_function()

logging.debug("This message goes to the file")
logging.info("So does this info message")
