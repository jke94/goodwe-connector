import logging

class GoodweApiLogger:

    def __init__(self, isLogging) -> None:
        
        logging.basicConfig(
            filename='goodwe-connector.log', 
            encoding='utf-8', 
            level=logging.DEBUG)
        
        self.__logging = isLogging
    
    def info(self, msg, *args, **kwargs):
        
        if (self.__logging):      
            logging.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        
        if (self.__logging):
            logging.warning(msg, *args, **kwargs)