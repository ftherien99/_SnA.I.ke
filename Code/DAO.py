from abc import ABC, abstractmethod

class DAO(ABC):

    @abstractmethod
    def dbConnection(self):
        pass

    @abstractmethod
    def dbCloseConnection(self):
        pass

    @abstractmethod
    def getHighscore(self):
        pass

    @abstractmethod
    def saveHighscore(self):
        pass

    @abstractmethod
    def getColors(self):
        pass

    @abstractmethod
    def saveColors(self):
        pass
