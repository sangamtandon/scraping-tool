from fastapi import FastAPI, Query, HTTPException, Header
from scraping.scraper import Scraper
from storage.database import JSONDatabase
from notification.notifier import ConsoleNotifier
from config import STATIC_TOKEN, RETRY_COUNT, RETRY_DELAY, CACHE_EXPIRY, URL, FILENAME
import time
from authentication.auth import Auth

# Instantiate the FastAPI app
app = FastAPI()

# Instantiate the Scraper class
scraper = Scraper()

# Instantiate the Database object
database = JSONDatabase(filename=FILENAME)

# Instantiate a notifier object
notifier = ConsoleNotifier()

# Instantiate the Auth class
auth = Auth(STATIC_TOKEN)

@app.get("/scrape")
async def scrape_data(
    max_pages: int = Query(None, title="Maximum number of pages to scrape"),
    proxy: str = Query(None, title="Proxy string for scraping"),
    x_token: str = Header(None)
):
    
    # Authenticate user
    if not auth.authenticate(x_token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Scrape data from the target website with retry mechanism
    retry_count = RETRY_COUNT
    while retry_count > 0:
        try:
            products = scraper.scrape_with_retry(URL, max_pages=max_pages, proxy=proxy)
            break  # Exit loop if scraping successful
        except Exception as e:
            print(f"Scraping failed. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
            retry_count -= 1
    else:
        return {"message": "Scraping failed after multiple retries."}

    if products:
        # Save data to database, considering caching mechanism
        database.save_data_with_caching(products, cache_expiry=CACHE_EXPIRY)
        
        return {"message": f"Scraping successful. Scraped {len(products)} products and saved to database."}
    else:
        return {"message": "Scraping failed."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
