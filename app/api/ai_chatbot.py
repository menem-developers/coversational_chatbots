from fastapi import APIRouter, HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai
import time

# Set up router
router = APIRouter()

# Configure Generative AI API
api_key = "AIzaSyASU__5e5ZTxpi-7WIGzg2TuAzQjzppqOA"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Define generation configuration and safety settings
generation_config = {
    "temperature": 0.1
}
safety_settings = [
    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

@router.post("/cinema_info/")
async def cinema_info(url: str, query: str):
    # Configure Selenium to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless for server environments
    chrome_options.add_argument("--no-sandbox")  # Recommended for Docker containers
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

    # Initialize WebDriver using webdriver-manager
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to the provided URL
        driver.get(url)
        time.sleep(5)  # Allow time for JavaScript to load

        # Extract relevant content (e.g., main article or content sections)
        # Here, you might want to adjust this selector to capture the main text
        page_content = driver.find_element(By.TAG_NAME, "body").text

        # Generate a response from the AI model
        response = model.generate_content([
            f"""
            You are an AI assistant specializing in cinema and music. Here is the content extracted from the provided webpage:
            
            "{page_content}"

            The user’s query is:
            '{query}'

            Based on the content from the webpage, answer the user’s query as accurately as possible.
            """
        ], safety_settings=safety_settings, generation_config=generation_config)

        response_text = response.text.strip()
        return {"generated_response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        driver.quit()  # Ensure driver is closed
