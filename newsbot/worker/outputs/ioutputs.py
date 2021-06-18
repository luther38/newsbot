from abc import ABC, abstractclassmethod
from typing import List


class IOutputs(ABC):
    def __init__(self):
        pass

    @abstractclassmethod
    def enableThread(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def buildMessage(self) -> None:
        raise NotImplementedError

    @abstractclassmethod
    def sendMessage(self) -> None:
        raise NotImplementedError
