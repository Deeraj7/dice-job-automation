from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

from .handlers.shadow_dom_handler import ShadowDOMHandler
from .handlers.job_handler import JobHandler
from .handlers.search_filter_handler import SearchAndFilter

class DiceAutomation:
    def __init__(self, driver, wait, username, password, keyword, max_applications):
        self.driver = driver
        self.wait = wait
        self.username = username
        self.password = password
        self.search_keyword = keyword
        self.max_applications = max_applications

    def login(self):
        """Handle login process"""
        try:
            print("Navigating to Dice login page...")
            self.driver.get("https://www.dice.com/dashboard/login")
            time.sleep(2)
            
            print("Logging in...")
            email_input = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[placeholder='Please enter your email']")
            ))
            email_input.clear()
            email_input.send_keys(self.username)
            email_input.send_keys(Keys.RETURN)
            time.sleep(1)
            
            password_input = self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[type='password']")
            ))
            password_input.clear()
            password_input.send_keys(self.password)
            password_input.send_keys(Keys.RETURN)
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"Login failed: {str(e)}")
            return False

    def get_job_listings(self):
        """Get all job listings from the current page"""
        try:
            # Wait for at least one job listing to be present
            self.wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[data-cy='card-title-link'].card-title-link")
            ))
            time.sleep(2)  # Additional wait for all listings to load
            
            # Find all job listings
            return self.driver.find_elements(By.CSS_SELECTOR, "a[data-cy='card-title-link'].card-title-link")
        except Exception as e:
            print(f"Error finding job listings: {str(e)}")
            return []

    def run(self):
        """Main method to run the automation"""
        try:
            if not self.login():
                raise Exception("Login failed")

            search_filter = SearchAndFilter(self.driver, self.wait)
            if not search_filter.perform_search(self.search_keyword):
                raise Exception("Search failed")

            if not search_filter.apply_filters():
                raise Exception("Filter application failed")

            shadow_dom_handler = ShadowDOMHandler(self.driver, self.wait)
            job_handler = JobHandler(self.driver, self.wait, shadow_dom_handler)
            
            applications_submitted = 0
            jobs_processed = 0
            job_index = 0
            
            while applications_submitted < self.max_applications and jobs_processed < 30:
                try:
                    print("Waiting for filtered job listings...")
                    job_listings = self.get_job_listings()
                    
                    if not job_listings:
                        print("No jobs found with current filters")
                        break
                        
                    if job_index >= len(job_listings):
                        print("No more job listings to process")
                        break
                    
                    print(f"\nTrying job {job_index + 1} of {len(job_listings)} visible listings...")
                    
                    # Scroll to and click the job listing
                    listing = job_listings[job_index]
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", listing)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", listing)
                    
                    if job_handler.apply_to_job():
                        applications_submitted += 1
                        print(f"Successfully applied to {applications_submitted} jobs")
                    else:
                        print(f"Skipped job {job_index + 1} - already applied or not available")
                    
                    jobs_processed += 1
                    job_index += 1
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"Error processing job listing: {str(e)}")
                    job_index += 1
                    jobs_processed += 1
                    continue
            
            print(f"\nCompleted! Applied to {applications_submitted} jobs, processed {jobs_processed} listings")
            
        except Exception as e:
            print(f"An error occurred: {str(e)}")