import logging
from pythonjsonlogger import jsonlogger
import sys

#get logger
logger=logging.getLogger()

#create formatter
#formatter=logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
formatter=jsonlogger.JsonFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s")
#create handlers
stream_handler=logging.StreamHandler(sys.stdout)
file_handler=logging.FileHandler('logs.log')#LOGS

#set formatters 
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

#add handlers to the logger
logger.handlers=[stream_handler,file_handler]

#set log-level
logger.setLevel(logging.INFO)