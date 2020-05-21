import logging
from logging import handlers
from datetime import datetime

logger= logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# handler= logging.FileHandler("log.txt")

handler= logging.handlers.TimedRotatingFileHandler('.\\log\\all.log',when='midnight',interval=1,backupCount=30)
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s ： %(message)s'))

error_handler=logging.FileHandler('.\\log\\error.log')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s - %(filename)s[:%(lineno)d] - %(message)s'))

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter('%(asctime)s-%(levelname)s ： %(message)s'))

logger.addHandler(handler)
logger.addHandler(error_handler)
logger.addHandler(console)



logger.debug("this is a debug log")
logger.info("this is a info log")
logger.warning("this is a warning log")
logger.error("this is a error log")
logger.critical("this is a critical log")
logger.info("this is a info log")

def create_num(all_num):
    a, b=0, 1
    current_num =0
    while current_num < all_num:
        yield a
        a, b  = b, a+b
        current_num +=1
obj =create_num(10)
for num in obj:
    print(num)

    
