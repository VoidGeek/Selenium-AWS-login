import os
import time
from selenium import webdriver
from dotenv import load_dotenv
from utils.error_handler import ErrorHandler


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

    def login_with_cookies(self):
        """Automate GitHub login using session cookies."""
        try:
            self.driver.get("https://github.com")
            self._add_cookies_to_browser()
            self.driver.refresh()
            time.sleep(5)
            print("Logged in successfully using cookies!")
        finally:
            self.driver.quit()
