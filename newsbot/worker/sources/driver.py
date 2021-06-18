from time import sleep
from newsbot.core.logger import Logger
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver import Firefox, FirefoxOptions
from os.path import exists
from os import remove
from abc import ABC, abstractclassmethod

class IDriver(ABC):
    @abstractclassmethod
    def driverStart(self) -> object:
        pass
    
class BDriver(IDriver):
    def __init__(self) -> None:
        self.logger = Logger(__class__)
        self.uri: str = ''
        self.driver: Firefox = self.driverStart()

    def driverGetContent(self) -> str:
        try:
            content = self.driver.page_source
            return content
        except Exception as e:
            if "Failed to decode response from marionette" in e.args[0]:
                self.logger.critical(f"Code: s01 - Failed to read from browser.  This can be due to not enough RAM on the system. Error: {e}")
            else:
                self.logger.critical(f"Failed to collect data from {self.uri}. {e}")

    def driverGoTo(self, uri: str) -> None:
        try:
            self.driver.get(uri)
            sleep(3)
            #self.driver.implicitly_wait(10)
        except Exception as e:
            self.logger.error(f"Driver failed to get {uri}. Error: {e}")

    def driverSaveScreenshot(self, path: str) -> None:
        try:
            if exists(path) == True:
                remove(path)
        except Exception as e:
            self.logger.error(f"Attempted to remove the old screenshot on disk, but failed. Error: {e}")

        try:
            self.driver.save_screenshot(path)
        except Exception as e:
            self.logger.error(f"Attempted to save a screenshot to '{path}', but failed to do so. Error: {e}")

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