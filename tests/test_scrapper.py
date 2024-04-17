# test_scraper.py
from app.scraping.scraper import Scraper
from app.storage.database import JSONDatabase
from app.notification.notifier import ConsoleNotifier

def test_scraper():
    # Set parameters
    url = "https://dentalstall.com/shop/"
    max_pages = 3  # Scrape only the first 3 pages
    proxy = ""  # Provide your proxy address and port
    filename = 'scraped_data.json'  # JSON file to save scraped data
    
    # Instantiate a database object
    database = JSONDatabase(filename=filename)
    
    # Instantiate a notifier object
    notifier = ConsoleNotifier()
    
    # Instantiate the Scraper class with database and notifier
    scraper = Scraper(database=database, max_pages=max_pages, proxy=proxy, notifier=notifier)
    
    # Scrape data from the target website
    products = scraper.scrape(url)
    
    if products:
        # Print or verify the scraped data
        for product in products:
            print(product)
    else:
        print("Scraping failed.")

if __name__ == "__main__":
    test_scraper()
