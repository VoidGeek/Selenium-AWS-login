import os
import requests
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to get the latest blog post and generate summary using OpenAI
def get_and_summarize_latest_post():
    # Initialize the WebDriver (Chrome)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://bshreekara.blogspot.com")  # Replace with the correct URL

    # Wait until the page is fully loaded by checking the presence of blog posts
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".post")))

        # Find the latest blog post (featured post usually appears first)
        latest_blog = driver.find_element(By.CSS_SELECTOR, ".post")  # Adjust if needed

        # Get the title and link of the latest blog post
        title = latest_blog.find_element(By.CSS_SELECTOR, "h3.post-title").text  # Modify selector to match title
        link = latest_blog.find_element(By.TAG_NAME, "a").get_attribute("href")  # Extract blog post link

        # Render/Display the latest post title and link
        print(f"Latest Blog Post Found: {title}")
        print(f"Link: {link}")

        # Open the blog post to extract HTML content
        driver.get(link)

        # Wait for the content to load completely
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".post-body")))

        # Extract the post content (assuming it's in a div with class 'post-body')
        post_body = driver.find_element(By.CSS_SELECTOR, ".post-body").get_attribute('innerHTML')

        # Use BeautifulSoup to parse the HTML and clean the content
        soup = BeautifulSoup(post_body, "html.parser")
        text_content = soup.get_text()  # Extracts the raw text without HTML tags

        # Extract image URLs
        images = extract_images(soup)

        # Print the full post content (for verification)
        print("\nFull Blog Post Content:")
        print(text_content[:500])  # Display the first 500 characters for brevity

        # Generate a summary using OpenAI API
        summary = generate_summary_openai(text_content)  # Function to generate summary
        print("\nSummary of the Post:")
        print(summary)

        # Generate and save HTML file
        generate_html_file(summary, images)

    except Exception as e:
        print(f"Error: {e}")

    # Close the browser session
    driver.quit()

# Function to generate a summary using OpenAI's API
def generate_summary_openai(text):
    try:
        # Using OpenAI's ChatCompletion API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"Summarize the following blog post in English:\n\n{text}"}
            ],
            model="gpt-4",  # Use GPT-4 model for summarization
        )

        # Correct way to access the summary
        summary = chat_completion.choices[0].message.content
        return summary
    except Exception as e:
        print(f"OpenAI Summarization Error: {e}")
        return "Summary not available."

# Function to extract image URLs from the blog post
def extract_images(soup):
    # Find all image tags and extract the 'src' attribute
    images = soup.find_all('img')
    image_urls = []
    for img in images:
        img_url = img.get('src')
        if img_url:
            image_urls.append(img_url)
    return image_urls

# Function to generate an HTML file with the summary and images
def generate_html_file(summary, images):
    try:
        # Define the file name for the HTML file
        file_name = "blog_post_summary.html"

        # Create HTML content with professional styling
        html_content = f"""
        <html>
        <head>
            <title>Blog Post Summary</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                    color: #333;
                    line-height: 1.6;
                }}
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #fff;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                }}
                h1 {{
                    text-align: center;
                    color: #2c3e50;
                }}
                h2 {{
                    color: #3498db;
                }}
                p {{
                    font-size: 1.1em;
                    margin-bottom: 20px;
                }}
                .images {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: center;
                }}
                .images img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    transition: transform 0.3s;
                }}
                .images img:hover {{
                    transform: scale(1.05);
                }}
                .image-container {{
                    width: 30%;
                    margin-bottom: 20px;
                }}
                @media (max-width: 768px) {{
                    .image-container {{
                        width: 100%;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Blog Post Summary</h1>
                <h2>Summary:</h2>
                <p>{summary}</p>
                <h2>Images:</h2>
                <div class="images">
        """
        
        # Add images to the HTML content
        for img_url in images:
            html_content += f"""
                <div class="image-container">
                    <img src="{img_url}" alt="Blog Post Image">
                </div>
            """
        
        html_content += """
                </div>
            </div>
        </body>
        </html>
        """

        # Write the HTML content to a file
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"\nHTML file saved to {file_name}")

        # Open the HTML file after saving
        open_html_file(file_name)

    except Exception as e:
        print(f"Error generating HTML file: {e}")

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
    get_and_summarize_latest_post()

if __name__ == "__main__":
    main()
