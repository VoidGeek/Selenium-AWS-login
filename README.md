# Selenium GitHub Login Automation with Environment Variables

This project automates logging into GitHub using Selenium by leveraging cookies stored securely in environment variables. The project utilizes `python-dotenv` for managing sensitive information like session cookies.

## Features

- Automates GitHub login using session cookies (`_gh_sess` and `user_session`).
- Securely manages sensitive information using `.env`.
- Enforces environment variable validation with `.env.example`.

## Prerequisites

1. Python 3.8 or higher.
2. Google Chrome installed.
3. ChromeDriver matching your Chrome version (download from [here](https://sites.google.com/chromium.org/driver/)).

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/repo-name.git
   cd repo-name
   ```

2. **Set Up Environment**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   - Create a `.env` file based on the `.env.example`
   - Securely manages sensitive information using `.env`.
   - Enforces environment variable validation with `.env.example`.

   ```bash
   cp .env.example .env
   ```

4. **Download ChromeDriver**

   - Ensure you have the correct version of ChromeDriver for your installed Chrome browser.

## Usage

1. **Obtain GitHub Cookies**:

   - Open your browser and log in to your GitHub account.
   - Press `F12` to open the developer tools.
   - Go to the **Application** tab (or **Storage** tab in some browsers).
   - Select **Cookies** from the left-hand menu and click on `https://github.com`.
   - Copy the values for the following cookies:
     - `_gh_sess`
     - `user_session`
   - Paste these values into the `.env` file under the keys `GH_SESS` and `USER_SESSION`.

2. **Update the `.env` File**:

   - Edit the `.env` file and add the copied cookie values:
     ```plaintext
     GH_SESS=your_gh_sess_value_here
     USER_SESSION=your_user_session_value_here
     ```

3. **Run the Automation Script**:

   - Execute the script to automate the login process:
     ```bash
     python script.py
     ```

4. **Observe Browser Behavior**:

   - The browser window will open.
   - The script will add the cookies (`_gh_sess` and `user_session`) to the session.
   - After refreshing, it will simulate an authenticated session and log in to your GitHub account.

5. **Verify the Output**:
   - Check the console for a success message:
     ```
     Logged in successfully using cookies!
     ```
