import logging

def setup_logger():
    # creating a logger instance
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # creating a handler to write log messages to a file
    file_handler = logging.FileHandler('calibration.log')
    file_handler.setLevel(logging.INFO)
    
    # creating a handler to output log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # setting the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # adding the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
