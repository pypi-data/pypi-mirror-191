import traceback

from app_common.helpers.bugs_helpers import post_error_on_slack

LOGGER_MAP = {}


class Logger:
    @staticmethod
    def create_logger(name):
        logger = LOGGER_MAP.get(name) or Logger(name)
        LOGGER_MAP[name] = logger
        return logger

    def __init__(self, name):
        self.name = name

    def info(self, message):
        print(f'INFO from {self.name} : {message}')

    def warning(self, message):
        print(f'WARNING in {self.name} : {message}')
        # post_error_on_slack('Warning', f'{self.name} : {message}')

    def error(self, message):
        try:
            tb = traceback.format_exc()
        except:
            tb = ''
        print(f'ERROR in {self.name} : {message}\n Stacktrace:-{tb}')
        post_error_on_slack('Error', f'{self.name} : {message}')
