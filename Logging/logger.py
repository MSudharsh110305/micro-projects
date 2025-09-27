import logging

# Setup a logger for the application
app_logger = logging.getLogger('app')
app_logger.setLevel(logging.DEBUG)

# Console handler (prints to screen)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Only INFO and above to console

# File handler (writes to file)
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)  # Debug and above to file

# Formatter with timestamp, logger name, level, function, line, and message
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to the logger
app_logger.addHandler(console_handler)
app_logger.addHandler(file_handler)

# Example functions using the logger
def divide(x, y):
    app_logger.debug(f"Attempting to divide {x} by {y}")
    try:
        result = x / y
        app_logger.info(f"Division successful: {result}")
        return result
    except ZeroDivisionError:
        app_logger.exception("Error: Division by zero occurred!")
        return None

def main():
    app_logger.info("Application started")
    divide(10, 2)
    divide(5, 0)
    app_logger.info("Application finished")

if __name__ == "__main__":
    main()
