from src.automation import DiceAutomation
from src.utils.webdriver_setup import setup_driver
from config import CREDENTIALS, SEARCH_SETTINGS

def main():
    driver = None
    try:
        # Setup WebDriver
        driver, wait = setup_driver()
        
        # Create automation instance
        automation = DiceAutomation(
            driver=driver,
            wait=wait,
            username=CREDENTIALS["username"],
            password=CREDENTIALS["password"],
            keyword=SEARCH_SETTINGS["keyword"],
            max_applications=SEARCH_SETTINGS["max_applications"]
        )
        
        # Run the automation
        automation.run()
        
        print("\nPress Enter to close the browser...")
        input()
        
    except Exception as e:
        print(f"\nScript failed with error: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()