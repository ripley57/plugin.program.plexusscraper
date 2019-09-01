
from selenium.webdriver.common.by import By
from browser import Browser


class HomePageLocator:
	URLS_PAGE = (By.XPATH, "//a[@href='plexus.php']")


class HomePage(Browser):
	def __init__(self, _browser):
		pass

