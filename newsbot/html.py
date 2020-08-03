from typing import List
import re


class Html:
    def __init__(self):
        pass

    def findByTag(self, tag: str, message: str):
        f: str = f"(?<=<{tag} )(.*)(?={tag}>)"
        results: List = re.findall(f, message)
