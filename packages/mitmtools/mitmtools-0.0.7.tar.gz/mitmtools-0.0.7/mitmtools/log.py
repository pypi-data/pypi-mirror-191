"""
    控制共有日志的打印，避免多个类重复输出（仅代码内的非模块）

    非共有的直接用 logger
"""
import threading
from loguru import logger


class Logger:
    LOCK = threading.RLock()
    LOG_STATUS = False

    def __init__(self):
        self.__class__.LOCK.acquire()
        if self.__class__.LOG_STATUS is False:
            self.__class__.LOG_STATUS = True
            self.log_status = True
        else:
            self.log_status = False
        self.__class__.LOCK.release()

    def debug(self, *args, sep: str = " "):
        self.log_status and logger.debug(f'{sep}'.join(args))

    def info(self, *args, sep: str = " "):
        self.log_status and logger.info(f'{sep}'.join(args))

    def warning(self, *args, sep: str = " "):
        self.log_status and logger.warning(f'{sep}'.join(args))

    def error(self, *args, sep: str = " "):
        self.log_status and logger.error(f'{sep}'.join(args))
