from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Chromedriver:
    """
    Base class for scraper classes that require a Selenium WebDriver to scrape
    the required information.
    """

    def __init__(self, chromedriver_url):
        self.chromedriver_url = chromedriver_url
        self.driver = self.__new_driver__()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __new_driver__(self):
        driver = webdriver.Remote(
            command_executor=f"http://{self.chromedriver_url}/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )

        return driver

    def close(self):
        self.driver.close()
