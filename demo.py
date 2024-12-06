import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time

# Load environment variables from the .env file (if you want to store credentials securely)
load_dotenv()

# Netflix login credentials (can also be stored in .env for security)
email = "keerthi.is21@sahyadri.edu.in"
password = "14072003Aa*"

# Initialize the WebDriver (Chrome)
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Function to log in to Netflix and render the page as HTML
def login_to_netflix():
    try:
        # Open Netflix login page
        driver.get("https://www.netflix.com/login")

        # Wait for the page to load
        time.sleep(3)

        # Find and input the email field using provided XPath
        email_field = driver.find_element(By.XPATH, '//*[@id=":r0:"]')
        email_field.send_keys(email)
        time.sleep(3)

        # Find and input the password field using provided XPath
        password_field = driver.find_element(By.XPATH, '//*[@id=":r3:"]')
        password_field.send_keys(password)

        # Find and click the submit button using a more stable CSS selector (e.g., by button's class or text)
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()

        # Wait for login to process (you can adjust the sleep time if necessary)
        time.sleep(5)

        print("Login Successful\n")
        # Capture the page HTML after login
        page_html = driver.page_source

        # Save the HTML content to a file
        save_html_to_file(page_html)

    except Exception as e:
        print(f"Error during login: {e}")
    finally:
        # Close the browser after some time
        time.sleep(5)
        driver.quit()

# Function to save the HTML page source to a file
def save_html_to_file(html_content):
    try:
        # Define the file name for the HTML file
        file_name = "netflix_home_page.html"

        # Save the HTML content to the file
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"\nHTML file saved to {file_name}")

        # Open the HTML file after saving
        open_html_file(file_name)

    except Exception as e:
        print(f"Error saving HTML file: {e}")

# Function to open the HTML file in the browser
def open_html_file(file_name):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_name)
        elif os.name == 'posix':  # macOS or Linux
            os.system(f"open {file_name}")  # macOS
            # os.system(f"xdg-open {file_name}")  # For Linux
        time.sleep(2)  # Wait a bit for the file to open
    except Exception as e:
        print(f"Error opening the HTML file: {e}")

# Main function to run the script
def main():
    login_to_netflix()

if __name__ == "__main__":
    main()
