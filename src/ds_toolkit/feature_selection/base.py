from abc import ABC, abstractmethod


class BaseReport(ABC):

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def report(self):
        pass
