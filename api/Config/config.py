
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import os
class LoggerSetup:
    @staticmethod
    def setup_logging(app_name='app', log_dir='logs'):
       
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        logger = logging.getLogger(app_name)
        logger.setLevel(logging.DEBUG)
        
        detailed_format = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(funcName)s() | %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S'
        )
        
        all_logs_file = os.path.join(log_dir, f'{app_name}_all.log')
        all_handler = RotatingFileHandler(
            all_logs_file,
            maxBytes=10 * 1024 * 1024,  
            backupCount=10  
        )
        all_handler.setLevel(logging.DEBUG)
        all_handler.setFormatter(detailed_format)
        logger.addHandler(all_handler)
        
        error_logs_file = os.path.join(log_dir, f'{app_name}_errors.log')
        error_handler = RotatingFileHandler(
            error_logs_file,
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_format)
        logger.addHandler(error_handler)
        
        dated_logs_file = os.path.join(log_dir, f'{app_name}_daily.log')
        dated_handler = TimedRotatingFileHandler(
            dated_logs_file,
            when='midnight', 
            interval=1,
            backupCount=30  
        )
        dated_handler.setLevel(logging.INFO)
        dated_handler.setFormatter(detailed_format)
        logger.addHandler(dated_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        logger.info(f"Logger '{app_name}' configuré avec succès")
        logger.debug(f"Fichiers de log dans: {os.path.abspath(log_dir)}")
        
        return logger
