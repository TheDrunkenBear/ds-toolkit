from abc import ABC, abstractmethod


class BaseFeatureSelection(ABC):

    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    def report(self):
        pass

    @staticmethod
    @abstractmethod
    def visualization(self):
        pass

