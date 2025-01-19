import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyCmGBW9Ucu7uoMZHGFotx4VQpkAgzn93Lo')
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', 'C:/Users/saket/OneDrive/Desktop/scrape/chromedriver-win64/chromedriver.exe')
    CACHE_TIMEOUT = int(os.getenv('CACHE_TIMEOUT', 3600))  # 1 hour cache
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30)) 