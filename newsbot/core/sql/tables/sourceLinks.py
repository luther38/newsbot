from newsbot.core.sql.tables.schema import Sources
from typing import List
from sqlalchemy.orm.session import Session
from newsbot.core.constant import SourceName, SourceType
from newsbot.core.sql import database
from newsbot.core.sql.tables.sources import SourcesTable
from newsbot.core.sql.tables import ITables, DiscordWebHooksTable, SourceLinks, discordWebHooks
from newsbot.core.sql.exceptions import FailedToAddToDatabase

class SourceLinksTable(ITables):
    def __init__(self, session: Session) -> None:
        self.setSession(session)

    def setSession(self, session: Session) -> None:
        self.s = session
        self.sourceTable = SourcesTable(session=self.s)
        self.discordTable = DiscordWebHooksTable(session=self.s)

    def __convertFromEnum__(self, item:Sources) -> Sources:
        item.source = item.source.value
        item.type = item.type.value
        return item

    def __convertToEnum__(self, item: Sources) -> Sources:
        item.source = SourceName.fromString(item.source)
        item.type = SourceType.fromString(item.type)
        return item

    def __filterDupes__(self, items: List[SourceLinks]) -> List[SourceLinks]:
        newList: List[SourceLinks] = list()
        for i in items:
            isDupe = False
            for nl in newList:
                if i.discordName == nl.discordName:
                    isDupe = True
            if isDupe == False:
                newList.append(i)
        return newList

    def __len__(self) -> int:
        """
        Returns the number of rows based off the name value provided.

        Returns: Int
        """
        l = list()
        try:
            for res in self.s.query(SourceLinks):
                l.append(res)
        except Exception as e:
            pass
        return len(l)

    def add(self, item: SourceLinks) -> None:
        try:
            self.s.add(item)
            self.s.commit()
        except FailedToAddToDatabase as e:
            print(f"Failed to add {self.name} to 'SourceLinks'. {e}")

    def update(self, item: SourceLinks) -> None:
        """
        This looks for at the name column to find an existing record.
        If it does not find a record, it will look up based off the SourceID given to see if something exists for that source.
        """
        wasUpdated: bool = False
        try:
            fromDb = self.findBySourceNameAndType(name=item.sourceName, type=item.sourceType)

            if fromDb.sourceName != '':
                # the record was found, lets update this one
                source = self.sourceTable.findByNameandSource(name=item.sourceName, source=item.sourceType)
                discord = self.discordTable.findByName(name=item.discordName)

                if source.source != '':
                    if fromDb.sourceID != source.id:
                        item.sourceID = source.id
                        wasUpdated = True

                if discord.name != '':
                    if fromDb.discordID != discord.id:
                        item.discordID = discord.id
                        wasUpdated = True
                
                if wasUpdated == True:
                    self.add(fromDb)
                    
            else:
                # we did not find an existing record, just add a new one.
                self.add(item)
        except Exception as e:
            print(e)
            pass

    def findAllByName(self, name: str) -> List[SourceLinks]:
        """
        Searches the database for objects that contain the name value.
        
        Returns: List[SourceLinks]
        """
        l = list()
        try:
            for res in self.s.query(SourceLinks).filter(SourceLinks.name.contains(name)):
                l.append(res)
        except Exception as e:
            pass
        return l

    def findAllBySourceType(self, sourceType: str) -> List[SourceLinks]:
        """
        Searches the database for objects that contain the source value.
        
        Returns: List[SourceLinks]
        """
        l = list()
        try:
            for res in self.s.query(SourceLinks).filter(SourceLinks.sourceType.contains(sourceType)):
                l.append(res)
        except Exception as e:
            pass
        return l

    def findAllBySourceNameAndType(self, name: str, type: str ) -> List[SourceLinks]:
        l = list()
        try:
            for d in self.s.query(SourceLinks).filter(
                SourceLinks.sourceName.contains(name),
                SourceLinks.sourceType.contains(type)
                ):
                l.append(d)
        except Exception as e:
            pass
        return l

    def findByName(self, name: str) -> SourceLinks:
        try:
            for res in self.s.query(SourceLinks).filter(SourceLinks.name == name):
                return res
        except Exception as e:
            pass
        return SourceLinks()

    def findBySourceNameAndType(self, name: str, type: str ) -> SourceLinks:
        d = SourceLinks()
        try:
            for d in self.s.query(SourceLinks).filter(
                SourceLinks.sourceName.contains(name),
                SourceLinks.sourceType.contains(type)
                ):
                return d
        except Exception as e:
            pass
        return SourceLinks()
    
    def findBySourceID(self, sourceID: str) -> SourceLinks:
        try:
            for res in self.s.query(SourceLinks).filter(SourceLinks.sourceID == sourceID):
                return res
        except Exception as e:
            pass
        return SourceLinks()

    def findSingleByName(self, name: str ) -> SourceLinks:
        """
        Searches the database for objects that contain the name value.
        Returns: SourceLinks
        """
        try:
            for d in self.s.query(SourceLinks).filter(SourceLinks.name.contains(name)):
                return d
                pass
        except Exception as e:
            pass
        return SourceLinks()
    
    def findByDiscordName(self, discordName: str ) -> SourceLinks:
        d = SourceLinks()
        try:
            for d in self.s.query(SourceLinks).filter(SourceLinks.discordName.contains(discordName)):
                return d
        except Exception as e:
            pass
        return SourceLinks()

    def findByDiscordID(self, discordID: str) -> SourceLinks:
        try:
            for res in self.s.query(SourceLinks).filter(SourceLinks.discordID == discordID):
                return res
        except Exception as e:
            pass
        return SourceLinks()

    def clearTable(self) -> None:
        """
        Removes all the objects found in the SourceLinks Table.

        Returns: None
        """
        try:
            for d in self.s.query(SourceLinks):
                self.s.delete(d)
            self.s.commit()
        except Exception as e:
            print(f"{e}")

    def clearByID(self, id: str) -> bool:
        """
        This will remove a single entry from the table by its ID value.
        """
        result: bool = False
        try:
            for i in self.s.query(SourceLinks).filter(SourceLinks.id == id):
                self.s.delete(i)
                self.s.commit()
                result = True
        except Exception as e:
            print(e)
        return result


