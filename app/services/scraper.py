from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
import time
from ..utils.helpers import retry_on_exception

class ReviewScraper:
    def __init__(self, driver_path, llm_service):
        self.driver_path = driver_path
        self.llm_service = llm_service
        self.options = webdriver.ChromeOptions()
        
        # Basic options
        self.options.add_argument('--headless=new')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        
        # Handle WebGL and graphics
        self.options.add_argument('--disable-software-rasterizer')
        self.options.add_argument('--disable-webgl')
        self.options.add_argument('--disable-webgl2')
        
        # Additional performance options
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-logging')
        self.options.add_argument('--disable-in-process-stack-traces')
        self.options.add_argument('--log-level=3')
        
        # Experimental options
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_experimental_option('prefs', {
            'profile.default_content_setting_values.images': 2,
            'profile.default_content_settings.popups': 0,
            'profile.managed_default_content_settings.images': 2,
            'disk-cache-size': 4096
        })
        
        self.max_retries = 3
        self.page_load_timeout = 10

    @retry_on_exception(max_retries=3)
    def extract_reviews(self, url):
        driver = self.setup_driver()
        try:
            driver.get(url)
            selectors = self.llm_service.get_selectors(driver.page_source)
            
            seen_reviews = set()
            reviews = []
            page = 1
            
            while True:
                time.sleep(2)
                page_reviews = self.get_review_elements(driver, selectors)
                
                if page_reviews:
                    reviews_on_page = 0
                    duplicates_on_page = 0
                    
                    for element in page_reviews:
                        review_data = self.extract_review_data(element, selectors['selectors'])
                        if review_data:
                            review_key = f"{review_data['reviewer']}_{review_data['title']}_{review_data['body']}"
                            if review_key not in seen_reviews:
                                seen_reviews.add(review_key)
                                reviews.append(review_data)
                                reviews_on_page += 1
                
                if len(reviews) >= 1000:
                    break
                    
                if not self.go_to_next_page(driver, selectors['next_button']):
                    break
                
                page += 1

            return {
                "reviews_count": len(reviews),
                "reviews": reviews,
                "pages_scraped": page
            }

        finally:
            driver.quit()

    def setup_driver(self):
        service = webdriver.chrome.service.Service(self.driver_path)
        return webdriver.Chrome(service=service, options=self.options)

    def get_review_elements(self, driver, selectors):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selectors['review_item']))
            )
            return driver.find_elements(By.CSS_SELECTOR, selectors['review_item'])
        except TimeoutException:
            return []

    def extract_review_data(self, element, selectors):
        try:
            return {
                "title": element.find_element(By.CSS_SELECTOR, selectors['title']).text,
                "body": element.find_element(By.CSS_SELECTOR, selectors['content']).text,
                "rating": self.extract_rating(element, selectors['rating']),
                "reviewer": element.find_element(By.CSS_SELECTOR, selectors['author']).text
            }
        except Exception:
            return None

    def extract_rating(self, element, rating_selector):
        try:
            rating_element = element.find_element(By.CSS_SELECTOR, rating_selector)
            rating_text = rating_element.get_attribute('aria-label') or rating_element.text
            return int(float(next(num for num in rating_text.split() if num.replace('.', '').isdigit())))
        except Exception:
            return 0

    def go_to_next_page(self, driver, next_button_selector):
        try:
            selectors = [
                '[aria-label="Goto next page"]',
                'button[aria-label="Next page"]',
                next_button_selector,
                'button.next-page',
                'a.next-page',
                '[class*="pagination"] [class*="next"]'
            ]
            
            for selector in selectors:
                try:
                    next_button = WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    
                    if 'disabled' in next_button.get_attribute('class').lower():
                        continue
                    
                    driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
                        next_button
                    )
                    time.sleep(1)
                    
                    for _ in range(3):
                        try:
                            next_button.click()
                            break
                        except:
                            driver.execute_script("arguments[0].click();", next_button)
                    
                    time.sleep(2)
                    return True
                    
                except Exception:
                    continue
            
            return False
            
        except Exception:
            return False