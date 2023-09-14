from sys import stderr

from loguru import logger


logger.remove()
logger.add(
    stderr, 
    format='<white>{time:HH:mm:ss}</white>'
        ' | <bold><level>{level: <7}</level></bold>'
        ' | <cyan>{line: <3}</cyan>'
        ' | <white>{message}</white>'
)
logger.add('logger.log')
