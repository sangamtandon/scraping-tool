from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, database=None, proxy=None, notifier=None):
        self.database = database
        self.total_products_scraped = 0
        self.notifier = notifier
        self.max_pages = None
        self.proxy = None

    def scrape_with_retry(self, url, max_pages=None, proxy=None):
        if max_pages is not None:
            self.max_pages = max_pages
        if proxy is not None:
            self.proxy = proxy

        try:
            products = []
            page_count = 1
            while True:
                print(f"Scraping product data from Page {page_count}")
                response = self.make_request(url)
                if not response:
                    break
                soup = BeautifulSoup(response.text, 'html.parser')
                product_cards = soup.find_all('div', class_='product-inner')
                for card in product_cards:
                    product_title = card.find('h2', class_='woo-loop-product__title')
                    product_title = product_title.text.strip() if product_title else "Unknown"

                    product_price = card.find('span', class_='woocommerce-Price-amount')
                    product_price = float(product_price.text.strip().replace('₹', '')) if product_price else 0.0

                    product_image = card.find('div', class_='mf-product-thumbnail').find('img')
                    product_image = product_image['data-lazy-src'] if product_image and 'data-lazy-src' in product_image.attrs else "No Image"

                    products.append({
                        "product_title": product_title,
                        "product_price": product_price,
                        "path_to_image": product_image
                    })

                next_page_link = soup.find('a', class_='next page-numbers')
                if not next_page_link or (self.max_pages and page_count >= self.max_pages):
                    break
                url = next_page_link['href']
                page_count += 1

            self.total_products_scraped += len(products)
            return products

        except Exception as e:
            print(f"An error occurred while scraping {url}: {str(e)}")
            return None

    def make_request(self, url):
        try:
            if self.proxy:
                response = requests.get(url, proxies={'http': self.proxy, 'https': self.proxy})
            else:
                response = requests.get(url)
            if response.status_code == 200:
                return response
            else:
                print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred while making request to {url}: {str(e)}")
            return None
