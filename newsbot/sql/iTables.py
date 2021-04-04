from typing import List

class ITables():
    def __init__(self) -> None:
        pass

    def add(self) -> None:
        raise NotImplementedError()
    def update(self) -> bool:
        raise NotImplementedError()

    def clearTable(self) -> None:
        raise NotImplementedError()
    def clearSingle(self) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        raise NotImplementedError()
        
    def findById(self) -> object:
        """
        This will look and return the object based off the ID value.
        """
        raise NotImplementedError()
    def findAllByName(self) -> List:
        raise NotImplementedError()

    def __len__(self) -> int:
        """
        Returns the total number of rows.
        """
        raise NotImplementedError()
