from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Class to extract links from a credit card listing page
class ExtractLinks:
    def __init__(self, url: str):
        # Initialize with the URL of the credit card listing page
        self.url = url
    
    # Function to extract relevant credit card links from the page
    def do_extraction(self):
        try:
            # Setup the WebDriver with headless Chrome options
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)

            # Open the provided URL
            driver.get(self.url)
            time.sleep(2)

            # Find the section containing all the credit card links
            all_cards_section = driver.find_element(By.ID, "all")
            card_links = all_cards_section.find_elements(By.TAG_NAME, "a")

            unique_links = set()

            # Loop through all the found links and filter them
            for link in card_links:
                href = link.get_attribute("href")
                if (
                    href and
                    "/credit-cards/" in href and
                    (
                        href.endswith(".page") or href.endswith(".com")
                    ) and
                    "eapply" not in href and
                    "apply" not in href
                ):
                    unique_links.add(href)
            
            # For testing purposes, uncomment this dummy list for static testing
            # dummy_list = ['https://www.sbicard.com/en/personal/credit-cards/lifestyle/doctors-sbi-card.page',
            #               'https://www.sbicard.com/en/personal/credit-cards/travel/club-vistara-sbi-card-prime.page',
            #               'https://www.sbicard.com/en/personal/credit-cards/shopping/titan-sbi-card.page',
            #               'https://www.sbicard.com/en/personal/credit-cards/shopping/reliance-sbi-card.page',
            #               'https://www.sbicard.com/en/personal/credit-cards/travel/paytm-sbi-card-select.page']
            
            # Return the extracted unique links as a list
            return list(unique_links)
            
        
        except Exception as e:
            print(f'Error extracting links: {e}')
    

# Run extraction when the script is executed directly
if __name__ == "__main__":
    test = ExtractLinks(url='https://www.sbicard.com/en/personal/credit-cards.page')
    print(test.do_extraction())
