import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    1 / 0
except ZeroDivisionError:
    logging.exception("Oops! Division by zero error")
