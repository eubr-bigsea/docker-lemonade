import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the root logger level to the lowest desired level

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M:%S')

    # Create a stream handler for displaying log messages on the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    path = '/app/logs/'
    # Create file handlers for writing log messages to separate files based on the log level
    file_handler_debug = logging.FileHandler(path + 'debug.log')
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_debug.setFormatter(formatter)

    file_handler_info = logging.FileHandler(path + 'info.log')
    file_handler_info.setLevel(logging.INFO)
    file_handler_info.setFormatter(formatter)

    file_handler_warning = logging.FileHandler(path + 'warning.log')
    file_handler_warning.setLevel(logging.WARNING)
    file_handler_warning.setFormatter(formatter)

    file_handler_error = logging.FileHandler(path + 'error.log')
    file_handler_error.setLevel(logging.ERROR)
    file_handler_error.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler_debug)
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_warning)
    logger.addHandler(file_handler_error)

    return logger
