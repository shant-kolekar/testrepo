import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class Glassdoor():
    """
    Glassdoor is a web scraper for glassdoor.com. 
    
    It is used to scrape Interview Questions for non-technical roles for eaxample: HR, Marketing, Sales, etc.
    """

    # Start of Glassdoor class methods
    def __init__(self, credentials):
        """
        You must have a Glassdoor account to use this scraper. 
        You must have signed up for an account with an email and password, not Google or Facebook.

        Provide credentials for Glassdoor in the following format:
        {
            "email": "email",
            "password": "password"
        }
        """

        # Create a new instance of Chrome driver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.delay = 10

        # Load credentials
        self.email = credentials["email"]
        self.password = credentials["password"]

    def __str__(self) -> str:
        """
        Return a string representation of the Glassdoor instance.
        """
        return f"Glassdoor(email={self.email}, password={self.password})"
    
    def __del__(self):
        """
        Close the current window when the Glassdoor instance is destroyed.
        """
        # Close the current window
        self.driver.close()
    
    # Start of Glassdoor helper methods
    def get_driver(self):
        """
        Return the current driver.
        """
        return self.driver

    def close_driver(self):
        """
        Close the current driver.
        """
        self.driver.close()
    
    def maximize_window(self):
        """
        Maximize the current window.
        """
        self.driver.maximize_window()
    
    def take_me_to(self, url):
        """
        Take me to the given URL.
        """
        self.driver.get(url)

    def get_sleep(self, sleep_time):
        """
        Sleep for the given time.
        """
        time.sleep(sleep_time)
    
    # Start of Glassdoor login methods             
    def glassdoor_login_url(self):
        """
        Return the Glassdoor login URL.
        """
        return "https://www.glassdoor.com/index.htm"

    def enter_email(self):
        """
        Enter the email into the email field. Return True if successful, False otherwise.
        """
        try:                
            # Find the email field
            email_field = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,\
                                                "input[id='inlineUserEmail']")))

            # Enter the email into the email field
            email_field.send_keys(self.email)

            print("Entered email.")

            return True
        
        except Exception as e:
            print("Error entering email.")
            print(e)
            return False
    
    def click_continue_with_email(self):
        """
        Click the "Continue with Email" button. Return True if successful, False otherwise.
        """
        try:
                
            # Find the "Continue with Email" button
            contine_with_email_button = WebDriverWait(self.driver, self.delay).\
                until(EC.element_to_be_clickable((By.CLASS_NAME, "emailButton")))

            # Click the "Continue with Email" button
            contine_with_email_button.click()

            print("Clicked continue with email button.")

            return True
        
        except TimeoutException:
            print("Timed out waiting for continue with email button.")
            return False
        except Exception as e:
            print("Error clicking continue with email button.")
            print(e)
            return False

    def enter_password(self):
        """
        Enter the password into the password field. Return True if successful, False otherwise.
        """
        try:                
           # Find the password field
            password_field = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, \
                                                "input[id='inlineUserPassword']"))
            )

            # Enter the password into the password field
            password_field.send_keys(self.password)

            print("Entered password.")

            return True
        
        except Exception as e:
            print("Error entering password.")
            print(e)
            return False

    def getInnerHtml(self, element):
        """
        Return the inner HTML of the given element.
        """
        try:
            return element.get_attribute("innerHTML")
        except Exception as e:
            print("Error getting inner HTML.")
            print(e)
            return None
        
    def getTagName(self, element):
        """
        Return the tag name of the given element.
        """
        try:
            return element.tag_name
        except Exception as e:
            print("Error getting tag name.")
            print(e)
            return None

    def getInnerElements(self, element, tag_name):
        """
        Return the inner elements of the given element.
        """
        try:
            return element.find_elements(By.TAG_NAME, tag_name)
        except Exception as e:
            print("Error getting inner elements.")
            print(e)
            return None

    def click_sign_in(self):
        """
        Click the "Sign In" button. Return True if successful, False otherwise.
        """
        try:
            all_buttons = self.driver.find_elements(By.XPATH, "//button")
            sign_in_button = None

            for button in all_buttons:
                for span in self.getInnerElements(button, "span"):
                    if 'Sign In' in self.getInnerHtml(span):
                        sign_in_button = button
            
            WebDriverWait(self.driver, self.delay+40).until(EC.element_to_be_clickable(sign_in_button))


            # Click the "Sign In" button
            sign_in_button.click()

            print("Clicked sign in button.")

            return True
        
        except TimeoutException:
            print("Timed out waiting for sign in button.")
            return False
        except Exception as e:
            print("Error clicking sign in button.")
            print(e)
            return False

    def login(self):
        """
        Login to Glassdoor using the provided credentials. Return True if successful, False otherwise.
        """
        try:
            # Go to the Glassdoor login page
            self.take_me_to(self.glassdoor_login_url())

            self.get_sleep(5)

            # Enter the email into the email field
            self.enter_email()

            self.get_sleep(5)

            # Click the "Continue with Email" button
            self.click_continue_with_email()

            self.get_sleep(5)
            
            # Enter the password into the password field
            self.enter_password()

            self.get_sleep(5)   

            # Click the "Sign In" button
            self.click_sign_in()

            print("Successfully logged in.")

            self.get_sleep(10)

            return True
        
        except Exception as e:
            print("Error logging in.")
            print(e)
            return False
    
    # Start of Glassdoor interview questions methods
    
