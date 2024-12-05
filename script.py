from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv()

# Retrieve cookie values from environment variables
gh_sess = os.getenv("GH_SESS")
user_session = os.getenv("USER_SESSION")

if not gh_sess or not user_session:
    raise ValueError("Missing GH_SESS or USER_SESSION in environment variables.")

# Initialize WebDriver
driver = webdriver.Chrome()

try:
    # Open GitHub homepage (required before adding cookies)
    driver.get("https://github.com")

    # Add cookies with the provided values
    cookies = [
        {"name": "_gh_sess", "value": gh_sess, "domain": ".github.com"},
        {"name": "user_session", "value": user_session, "domain": ".github.com"}
    ]
    for cookie in cookies:
        driver.add_cookie(cookie)

    # Refresh the page to apply cookies and verify the login
    driver.refresh()

    time.sleep(5)  # Wait to observe the result
    print("Logged in successfully using cookies!")

finally:
    # Close the browser
    driver.quit()
