from typing import Optional

from PyQt5.QtCore import QMutex, QWaitCondition


class WaitingData:
    def __init__(self):
        self.__mutex = QMutex()
        self.__condition = QWaitCondition()

        self.__data = None

    def wait(self):
        self.__condition.wait(self.__mutex)

    def wakeup(self, *args):
        self.__condition.wakeAll()
        self.__data = args

    def get_data(self) -> Optional[tuple]:
        return self.__data
