# cache.py

import json
import redis

# Instantiate a Redis client for caching
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Function to update cache and return updated products
def update_cache(products):
    updated_products = []
    for product in products:
        cached_product = redis_client.get(product['product_title'])
        if cached_product:
            cached_product = json.loads(cached_product)
            if cached_product['product_price'] != product['product_price']:
                # Price has changed, update cache
                redis_client.set(product['product_title'], json.dumps(product))
                updated_products.append(product)
        else:
            # Product not in cache, add to cache
            redis_client.set(product['product_title'], json.dumps(product))
            updated_products.append(product)
    return updated_products
