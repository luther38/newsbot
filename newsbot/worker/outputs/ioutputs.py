from abc import ABC, abstractclassmethod
from typing import List


class IOutputs(ABC):
    @abstractclassmethod
    def enableThread(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def enableTables(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def buildMessage(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def sendMessage(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def isSafeToRemove(self) -> bool:
        raise NotImplementedError

    @abstractclassmethod
    def threadWait(self) -> None:
        raise NotImplementedError