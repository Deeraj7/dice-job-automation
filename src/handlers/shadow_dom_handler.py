from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ShadowDOMHandler:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def find_and_click_easy_apply(self):
        """Find and click Easy Apply button within shadow DOM"""
        print("Attempting to find Easy Apply button in shadow DOM...")
        try:
            shadow_host = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "apply-button-wc.hydrated"))
            )
            print("Found shadow host element")
            
            button_clicked = self.driver.execute_script("""
                const shadowHost = arguments[0];
                const shadowRoot = shadowHost.shadowRoot;
                const easyApplyButton = shadowRoot.querySelector('button.btn.btn-primary');
                if (easyApplyButton && easyApplyButton.innerText.toLowerCase().includes('easy apply')) {
                    easyApplyButton.click();
                    return true;
                }
                return false;
            """, shadow_host)
            
            if button_clicked:
                print("Successfully clicked Easy Apply button")
                return True
            else:
                print("Easy Apply button not found - job might be already applied to")
                return False
                
        except Exception as e:
            print(f"Error finding Easy Apply button in shadow DOM: {str(e)}")
            return False