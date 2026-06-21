from abc import ABC, abstractmethod


class BaseLoginScenario(ABC):
    @abstractmethod
    def testEmail(self):
        pass

    @abstractmethod
    def testPassword(self):
        pass


class BaseRegistrationScenario(ABC):
    @abstractmethod
    def testFullName(self):
        pass

    @abstractmethod
    def testEmail(self):
        pass

    @abstractmethod
    def testPassword(self):
        pass

    @abstractmethod
    def testPasswordConfirmation(self):
        pass

    @abstractmethod
    def testPhoneNumber(self):
        pass
    

class BaseJobScenario(ABC):
    @abstractmethod
    def testSearchJob(self): pass

    @abstractmethod
    def testApplyJob(self): pass