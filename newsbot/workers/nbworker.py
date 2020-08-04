class NBWorker:
    def __init__(self):
        pass

    def check(self) -> bool:
        raise NotImplementedError

    def init(self) -> None:
        raise NotImplementedError
