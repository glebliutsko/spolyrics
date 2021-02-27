import logging
from typing import Optional

from PyQt5.QtCore import QMutex, QWaitCondition


class WaitingData:
    def __init__(self):
        self.logger = logging.getLogger('spolyrics')

        self.__mutex = QMutex()
        self.__condition = QWaitCondition()

        self.__data = None

    def wait(self):
        self.logger.debug(f'Lock: {self}')
        self.__condition.wait(self.__mutex)

    def wakeup(self, *args):
        self.__condition.wakeAll()
        self.__data = args

        self.logger.debug(f'Unlock: {self}. Data: {args}')

    def get_data(self) -> Optional[tuple]:
        return self.__data
