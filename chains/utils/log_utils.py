"""Log utilities that might be useful"""
import os
import logging

def get_logger():
    """Setup logging output defaults"""

    # Grab the logger
    if not hasattr(get_logger, 'logger'):

        # Setup the default logging config
        get_logger.logger = logging.getLogger('chains')
        format_str = '%(asctime)s [%(levelname)s] - %(module)s: %(message)s'
        logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO, format=format_str)

    # Return the logger
    return get_logger.logger

def panic(mesg):
    """Throw a critical message and raise a runtime exceptions"""
    get_logger().critical(mesg)
    raise RuntimeError(mesg)

def test_utils():
    """Test the utility methods"""
    logger = get_logger()
    logger.debug('Test debug log message')
    logger.info('Test information log message')
    logger.warn('Test warning log message')
    logger.error('Test error log message')
    logger.critical('Test critical log message')
    print 'Success!'

if __name__ == '__main__':
    test_utils()
