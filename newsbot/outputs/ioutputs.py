from typing import List


class IOutputs:
    def __init__(self):
        pass

    def enableThread(self) -> None:
        raise NotImplementedError

    def buildMessage(self) -> None:
        raise NotImplementedError

    def sendMessage(self) -> None:
        raise NotImplementedError
