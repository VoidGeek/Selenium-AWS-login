from services.github_login import GitHubLoginAutomation
from utils.error_handler import ErrorHandler


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
