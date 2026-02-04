import os
import django
import requests
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Factory.settings')
django.setup()

from main.models import Product

def download_and_update(product_name, url, filename):
    print(f"Attempting to update {product_name}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            product = Product.objects.filter(name=product_name).first()
            if product:
                blob = BytesIO(response.content)
                product.image.save(filename, File(blob), save=True)
                print(f"Successfully updated {product_name}")
            else:
                print(f"Product {product_name} not found")
        else:
            print(f"Failed to download {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Error updating {product_name}: {e}")

updates = [
    {
        "name": "Men Navy T-Shirt",
        "url": "https://upload.wikimedia.org/wikipedia/commons/2/24/Blue_T-shirt.jpg",
        "filename": "men_navy_tshirt_real.jpg"
    },
    {
        "name": "Women Red Dress",
        "url": "https://upload.wikimedia.org/wikipedia/commons/4/42/Red_Dress_%285817296041%29.jpg",
        "filename": "women_red_dress_real.jpg"
    },
    {
        "name": "Kids Blue Hoodie",
        "url": "https://upload.wikimedia.org/wikipedia/commons/a/a3/Kid_in_hoodie.jpg",
        "filename": "kids_hoodie_real.jpg"
    }
]

if __name__ == "__main__":
    for item in updates:
        download_and_update(item["name"], item["url"], item["filename"])
