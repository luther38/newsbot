from typing import List
#from abc import ABC, abstractclassmethod

class ITables():
#    @abstractclassmethod
    def add(self) -> None:
        raise NotImplementedError()

#    @abstractclassmethod
    def update(self) -> bool:
        raise NotImplementedError()

#    @abstractclassmethod
    def clearTable(self) -> None:
        raise NotImplementedError()

#    @abstractclassmethod
    def clearSingle(self) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        raise NotImplementedError()

#    @abstractclassmethod
    def findById(self) -> object:
        """
        This will look and return the object based off the ID value.
        """
        raise NotImplementedError()

#    @abstractclassmethod
    def findAllByName(self) -> List:
        raise NotImplementedError()

#    @abstractclassmethod
    def __len__(self) -> int:
        """
        Returns the total number of rows.
        """
        raise NotImplementedError()

#    @abstractclassmethod
#    def toDict(self, item: object) -> dict:
#        raise NotImplementedError
#
#    @abstractclassmethod
#    def toListDict(self, items: List[object]) -> List[dict]:
#        raise NotImplementedError