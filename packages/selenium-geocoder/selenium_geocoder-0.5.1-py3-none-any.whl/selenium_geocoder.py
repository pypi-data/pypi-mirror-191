from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from enum import Enum

class Browsers(Enum):
    FIREFOX=1
    CHROME=2
    EDGE=3  

def choose_browser(browser:Browsers):
    if(browser==Browsers.FIREFOX):
        return webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    elif(browser==Browsers.CHROME):
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif(browser==Browsers.EDGE):
        options = webdriver.EdgeOptions()
        return webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()),options=options)

class Globe:
    def __init__(self, browser:Browsers):
        """
        Browsers:
        --------------
        Supported browsers:
        - ```Browsers.FIREFOX```
        - ```Browsers.CHROME```
        - ```Browsers.EDGE```
        """
        self.driver = choose_browser(browser=browser)
    
    def get_url(self, name:str) -> str:
        url = "https://www.google.co.in/maps/search/" + name
        self.driver.get(url)
        return self.driver.current_url

    def get_coordinate(self, name:str)->tuple:
        x = self.get_url(name=name)
        while(x == self.driver.current_url):
            continue
        lat,long = self.driver.current_url.split('@')[1].split(',')[:2]
        return float(lat),float(long)
    
    def get_coordinates(self, name:list)->list:
        values = list()
        for x in name:
            url = self.get_url(name=x)
            while(url == self.driver.current_url):
                continue
            lat,long = self.driver.current_url.split('@')[1].split(',')[:2]
            values.append([lat,long])
        return values
    
