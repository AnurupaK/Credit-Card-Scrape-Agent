from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Class for defining the input parameters required for the scraper tool
class CardScraperInput(BaseModel):
    url: str = Field(..., description="The URL of the credit cards listing page.")
    
# Class for implementing the credit card scraper tool
class CreditCardScraperTool(BaseTool):
    name: str = 'Credit Card Scraper tool'
    description: str = "Scrapes credit card pages from Card site and extracts key content sections."
    args_schema: Type[BaseModel] = CardScraperInput
    
    # Function to scrape credit card details from the provided URL
    def _run(self, url: str) -> Dict[str, str]:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options = options)

        driver.get(url)
        time.sleep(2)
        
        card_content = ''
        for class_name in ['content-section', 'signature-detail', 'fees-savings']:
            try:
                element = driver.find_element(By.CLASS_NAME, class_name)
                outer_html = element.get_attribute('outerHTML')
                card_content += f'\n<!-- {class_name} -->\n{outer_html}'
            except Exception:
                continue  
    
        driver.quit()
        return card_content
    
scrape_tool = CreditCardScraperTool()
if __name__ == "__main__":
    test_url = "https://www.sbicard.com/en/personal/credit-cards/travel/sbi-card-miles-prime.page"
    scrape_tool = CreditCardScraperTool()

    result = scrape_tool._run(url=test_url)

    print("\n--- Extracted Info ---\n")
    print(result)
