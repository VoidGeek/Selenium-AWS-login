# error_handler.py

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
