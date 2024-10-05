import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Dosyaya log yazmak için handler oluştur
    file_handler = logging.FileHandler('calibration.log')
    file_handler.setLevel(logging.INFO)
    
    # Konsola log yazmak için handler oluştur
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Log formatını ayarla
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Handlerları logger'a ekle
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
