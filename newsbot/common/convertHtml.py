
from typing import List
from re import findall

class ConvertHtml:
    """
    This class is used on outputs to clean up HTML code and replce objects with native formatting.
    """

    def __init__(self) -> None:
        pass

    def findAllImages(self, text: str) -> List[str]:
        """
        About:
        Returns all the img tags found in the given text.

        Returns:
        List[str]
        """
        imgs = findall("<img (.*?)>", text)
        return imgs

    def replaceImages(self, msg: str, replaceWith: str) -> str:
        """
        About:
        Replaces all img tags found with new text.

        Returns:
        str
        """
        imgs = findall("<img (.*?)>", msg)
        for i in imgs:
            replace = f"<img {i}>"
            msg = msg.replace(replace, replaceWith)
        return msg