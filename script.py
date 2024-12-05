import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv


class ErrorHandler:
    """Centralized Error Handler for the application."""
    @staticmethod
    def handle_error(exc):
        error_messages = {
            ValueError: "Configuration Error",
            RuntimeError: "Runtime Error"
        }

        error_type = type(exc)
        message = error_messages.get(error_type, "Unexpected Error")
        print(f"{message}: {exc}")
        exit(1)  # Exit the program after handling the error


class GitHubLoginAutomation:
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
        self.driver.get("https://github.com")
        self._add_cookies_to_browser()
        self.driver.refresh()
        time.sleep(5)
        print("Logged in successfully using cookies!")
        self.driver.quit()


class Application:
    """Main application wrapper with centralized error handling."""
    @staticmethod
    def run():
        try:
            github_automation = GitHubLoginAutomation()
            github_automation.login_with_cookies()
        except Exception as e:
            ErrorHandler.handle_error(e)


if __name__ == "__main__":
    Application.run()
