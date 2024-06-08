from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from Event.EventHandler import EventManager
from Event.UpdateStreamEventHandler import UpdateStreamEventHandler
from Event.UpdateHistoryNewEventHandler import UpdateHistoryNewEventHandler
from Configuration import Configuration
from time import sleep
import pickle
from Symbols import Symbols
import pyautogui


class PoDriver(webdriver.Chrome):
    def __init__(self):
        service = Service()
        options = Options()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        webdriver.Chrome.__init__(self, service=service, options=options)
        self.set_window_size(1300, 900)
        self.set_window_position(0, 0)
        self.scrolledDown = False

        try:
            self.get(Configuration.URL)
            self.load_cookies(Configuration.COOKIES_FILE)
            self.get(Configuration.URL)
        except FileNotFoundError:
            self.get(Configuration.URL)
            sleep(10)
            self.save_cookies(Configuration.COOKIES_FILE)

    def save_cookies(self, location: str):
        pickle.dump(self.get_cookies(), open(location, "wb"))

    def load_cookies(self, location: str):
        cookies = pickle.load(open(location, "rb"))
        for cookie in cookies:
            self.add_cookie(cookie)

    def call(self):
        self.find_element(by=By.CLASS_NAME, value=f'btn-call').click()

    def put(self):
        self.find_element(by=By.CLASS_NAME, value=f'btn-put').click()

    def getCurrentSymbol(self):
        symbol = self.find_element(by=By.CLASS_NAME, value='current-symbol').text
        return Symbols.get(symbol, 'unknown symbol')
    
    def tryNextFavoriteItem(self):
        self.scrolledDown = False
        favorites_div = self.find_element(By.CLASS_NAME, 'assets-favorites-list__in')
        favorites_elements = favorites_div.find_elements(By.XPATH, './*')
        for fav in favorites_elements:
            symbol = fav.get_attribute('data-id')
            if symbol == Configuration.SYMBOL:
                fav.click()
                sleep(1)


    def scrollCandles(self):
        screenHeight = pyautogui.size().height
        pyautogui.moveTo(200, int(screenHeight / 2))
        if not self.scrolledDown:
            pyautogui.scroll(-200)
            self.scrolledDown = True
        pyautogui.drag(400, 0, duration=0.11, button='left')
        sleep(1)
    
    def scrollToEnd(self):
        element = self.find_element(By.CLASS_NAME, 'scroll-to-end')
        actions = ActionChains(self)
        actions.move_to_element(element).click().perform()