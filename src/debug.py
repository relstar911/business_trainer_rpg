import logging

# Initialize these at the module level
DEBUG = True  # You might want to set this based on a configuration file or environment variable
UPDATE_INTERVAL = 100  # Adjust as needed
update_counter = 0

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Debug flag
DEBUG = True

# Counters for limiting debug output
update_counter = 0
UPDATE_INTERVAL = 60  # Only log every 60th update

def debug_print(message, force=False):
    global update_counter
    if DEBUG:
        update_counter += 1  # Increment counter for every call
        if force or update_counter % UPDATE_INTERVAL == 0:
            logger.debug(message)

def info_print(message):
    logger.info(message)

def warning_print(message):
    logger.warning(message)

def error_print(message):
    logger.error(message)
