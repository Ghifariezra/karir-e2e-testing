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
    def testSearchJob(self):
        pass

    @abstractmethod
    def testKeyword(self):
        pass
    
    @abstractmethod
    def testLocation(self):
        pass
    
    @abstractmethod
    def clickSearchButton(self):
        pass
    
class BaseApplyJobScenario(ABC):
    @abstractmethod
    def testApplyJob(self):
        pass
