import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class TelegramBotLogger:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TelegramBotLogger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance
    
    def _initialize_logger(self):
        """Initialize the logger with both file and console handlers."""
        self.logger = logging.getLogger('TelegramBot')
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler with rotation
        log_file = os.path.join(log_dir, 'telegram_bot.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message."""
        self.logger.critical(message)

# Create a singleton instance
logger = TelegramBotLogger() 