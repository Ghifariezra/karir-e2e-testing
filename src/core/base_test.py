from abc import ABC, abstractmethod
from core.driver import Driver


class BaseTest(ABC):
    def __init__(self):
        self.driver = Driver().get_driver()

    @abstractmethod
    def formRegistration(self):
        pass

    @abstractmethod
    def formLogin(self):
        pass

    @abstractmethod
    def formSearch(self):
        pass

    @abstractmethod
    def formApply(self):
        pass
