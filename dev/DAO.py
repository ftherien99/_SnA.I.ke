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

    @abstractmethod
    def saveEpisode(self):
        pass

    @abstractmethod
    def getEpisodes(self):
        pass

    @abstractmethod
    def getEpisodeSteps(self):
        pass

    @abstractmethod
    def getEpisodeTime(self):
        pass

    @abstractmethod
    def getEpisodeScore(self):
        pass


    @abstractmethod
    def getEpisodeReward(self):
        pass

    @abstractmethod
    def createTables(self):
        pass