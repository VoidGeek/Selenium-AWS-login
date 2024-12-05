import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv


class GitHubLoginAutomation:
    """Handles GitHub login automation using cookies."""
    def __init__(self):
        """Initialize WebDriver and environment variables."""
        self.driver = webdriver.Chrome()
        load_dotenv()  # Load environment variables
        self.cookies = self._load_cookies()

    def _load_cookies(self):
        """Load cookies from environment variables."""
        gh_sess = os.getenv("GH_SESS")
        user_session = os.getenv("USER_SESSION")

        if not gh_sess or not user_session:
            raise ValueError("Missing required environment variables: GH_SESS or USER_SESSION.")

        return [
            {"name": "_gh_sess", "value": gh_sess, "domain": ".github.com"},
            {"name": "user_session", "value": user_session, "domain": ".github.com"}
        ]

    def _add_cookies_to_browser(self):
        """Add cookies to the browser session."""
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)

    def _validate_login(self):
        """Validate if login was successful using the provided XPath."""
        time.sleep(3)  # Wait for the page to load after refresh

        # Use the provided XPath to check for a logged-in user indicator
        login_indicator = self.driver.find_elements(By.XPATH, "/html/body/div[1]/div[5]/div/div/aside/div/div/loading-context/div/div[1]/div/div[1]/a")

        if not login_indicator:
            raise ValueError("Login validation failed. Cookies may be invalid or expired.")

        print("Login validation successful.")

    def login_with_cookies(self):
        """Automate GitHub login using session cookies."""
        self.driver.get("https://github.com")
        self._add_cookies_to_browser()
        self.driver.refresh()
        self._validate_login()
        print("Logged in successfully using cookies!")
        self.driver.quit()
