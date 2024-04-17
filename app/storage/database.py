from abc import ABC, abstractmethod
import json
from datetime import datetime, timedelta

class Database(ABC):
    def __init__(self, **kwargs):
        pass
    
    @abstractmethod
    def save_data(self, data):
        pass

class JSONDatabase:
    def __init__(self, filename):
        self.filename = filename

    def save_data_with_caching(self, data, cache_expiry):
        cached_data = self.load_cached_data()
        if cached_data:
            for product in data:
                existing_product = next((p for p in cached_data if p['product_title'] == product['product_title']), None)
                if existing_product and existing_product['product_price'] == product['product_price']:
                    continue  # Skip saving if product price hasn't changed
                else:
                    cached_data.append(product)
        else:
            cached_data = data

        self.save_data(cached_data)
        self.update_cache_timestamp(cache_expiry)

    def load_cached_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return None

    def save_data(self, data):
        try:
            with open(self.filename, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving data to {self.filename}: {str(e)}")

    def update_cache_timestamp(self, cache_expiry):
        timestamp = datetime.now() + timedelta(seconds=cache_expiry)
        with open('cache_timestamp.txt', 'w') as file:
            file.write(timestamp.isoformat())

class SQLDatabase(Database):
    def __init__(self, connection_string):
        self.connection_string = connection_string

    def save_data(self, data):
        # Implementation for saving data to a SQL database
        pass
    