"""Demonstrate how to create separate log files for each instance of a class.
"""
import logging
import os
import time


class MyClass():
    """Class to demonstrate separate log files for each instance.
    """

    def __init__(self):
        self.logger = None

    def start_log(self, logging_level: int = logging.INFO):
        """Allow each instance of this class to have a separate log file.

        :param int logging_level: The minimum logging level to log. \
            The default is INFO (20)

        :return: None
        """
        _log_dir = 'my_logs'
        if not os.path.exists(_log_dir):
            os.mkdir(_log_dir)

        _log_name = f"{self.__class__.__name__}_{time.time()}"
        _log_path = f"{_log_dir}/{_log_name}.log"
        _file_handler = logging.FileHandler(_log_path, mode='a', encoding='utf-8')
        _formatter = logging.Formatter(
            '\"%(asctime)s\", \"%(name)s\", \"%(levelname)s\", \"%(message)s\"')
        _file_handler.setFormatter(_formatter)

        self.logger = logging.getLogger(_log_name)
        self.logger.addHandler(_file_handler)
        self.logger.setLevel(logging_level)


if __name__ == '__main__':
    print('Starting instance logging test...')

    foo_class = MyClass()
    foo_class.start_log(logging.DEBUG)
    foo_class.logger.info('This is a test of foo.')

    # IMPORTANT! The name of the log file is the name of the class,
    # plus the time the class was instantiated (my_class_1725644384.38276.log).
    # Pause for a tenth of a second before creating a new log file
    # to prevent logs from having the same name.
    time.sleep(0.1)

    bar_class = MyClass()
    bar_class.start_log(logging.INFO)
    bar_class.logger.info('This is a test of bar.')

    bar_class.logger.debug(
        'I WILL NOT appear in bar, since it does not accept logging.DEBUG messages.')
    foo_class.logger.debug('I appear in foo, since it accepts logging.DEBUG messages.')

    bar_class.logger.warning('This is the end of bar.')
    foo_class.logger.warning('This is the end of foo.')

    print('End of test. Have a nice day.')
