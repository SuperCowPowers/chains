"""Log utilities that might be useful"""
import os
import logging

def log_defaults(log_level=logging.INFO, color=False):
    """Setup logging output defaults

        Args:
            log_level: set the log level (defaults to logging.INFO)
    """

    # Log format string
    format_str = '%(asctime)s [%(levelname)s] - %(module)s: %(message)s'

    # Set up all the logging defaults
    logging.basicConfig(datefmt='%Y-%m-%d %H:%M:%S', level=log_level, format=format_str)

    # Do they want colored logs
    if color:
        import coloredlogs
        coloredlogs.install(level=log_level)

def panic_and_throw(mesg):
    """Critical/panic message and raise Runtime Error

        Args:
            mesg: the message to send to logging.critical
        Returns:
            Raises a Runtime Error
    """
    logging.critical('PANIC: '+ mesg)
    raise RuntimeError(mesg)

def test_utils():
    """Test the utility methods"""
    log_defaults()
    logging.debug('Test debug log message')
    logging.info('Test information log message')
    logging.warn('Test warning log message')
    logging.error('Test error log message')
    logging.critical('Test critical log message')
    try:
        panic_and_throw('Remain Calm... nothing to see...')
        assert 0 # Getting here is 'wrong'
    except RuntimeError:
        print 'Success!'

if __name__ == '__main__':
    test_utils()
