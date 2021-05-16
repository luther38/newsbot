from newsbot.core.logger import Logger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from abc import ABC, abstractclassmethod

class IDriver(ABC):
    @abstractclassmethod
    def driverStart(self) -> object:
        pass
    
class BDriver(IDriver):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = ''
        self.driver = self.driverStart()

    def driverGetContent(self) -> str:
        try:
            return self.driver.page_source
        except Exception as e:
            self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def driverGoTo(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            self.driver.implicitly_wait(10)
        except Exception as e:
            self.logger.error(f"Driver failed to get {uri}. Error: {e}")

    def driverClose(self) -> None:
        try:
            self.driver.close()
        except Exception as e:
            self.logger.error(f"Driver failed to close. Error: {e}")

class BFirefox(BDriver):
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """

    def driverStart(self) -> Firefox:
        try:
            o = FirefoxOptions()
            o.headless = True
            driver = Firefox(options=o)
            return driver
        except Exception as e:
            self.logger.critical(f"Firefox driver failed to start: Error: {e}")


class BChrome(BDriver):
    """
    This class helps to interact with Chrome/Selenium.
    It was made to be used as a Base class for the sources who need Chrome.
    """

    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = ""
        self.driver = self.driverStart()
        pass

    def driverStart(self) -> Chrome:
        options = ChromeOptions()
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        try:
            driver = Chrome(options=options)
            return driver
        except Exception as e:
            self.logger.critical(f"Chrome Driver failed to start! Error: {e}")