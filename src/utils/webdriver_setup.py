from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

def setup_driver():
    """Initialize and configure the Chrome WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-notifications')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)
    return driver, wait