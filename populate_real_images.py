import os
import django
import requests
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Factory.settings')
django.setup()

from main.models import Product, Collection

def download_image(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def populate_collections():
    collections_data = [
        {
            "name": "Men", 
            "url": "https://images.unsplash.com/photo-1490114538077-0a7f8cb49891?q=80&w=1000&auto=format&fit=crop",
            "desc": "Latest fashion for men."
        },
        {
            "name": "Women", 
            "url": "https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=1000&auto=format&fit=crop",
            "desc": "Elegant and chic styles for women."
        },
        {
            "name": "Kids", 
            "url": "https://images.unsplash.com/photo-1519702202619-389335f6068d?q=80&w=1000&auto=format&fit=crop",
            "desc": "Fun and durable clothing for kids."
        },
        {
            "name": "Accessories", 
            "url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1000&auto=format&fit=crop",
            "desc": "Complete your look with our accessories."
        },
    ]

    print("Populating Collections...")
    for data in collections_data:
        collection, created = Collection.objects.get_or_create(name=data['name'])
        collection.description = data['desc']
        
        print(f"Updating Collection: {data['name']}")
        img_blob = download_image(data['url'])
        if img_blob:
            filename = f"collection_{data['name'].lower()}_final.jpg"
            collection.image.save(filename, File(img_blob), save=True)
            print(f"  -> Saved image for {data['name']}")
        else:
            print(f"  -> Failed to download image for {data['name']}")
        collection.save()

def populate_products():
    # Map specific products to real image URLs
    product_images = {
        "Men Navy T-Shirt": "https://source.unsplash.com/800x1000/?mens-tshirt",
        "Men Denim Jeans": "https://source.unsplash.com/800x1000/?jeans",
        "Men Leather Jacket": "https://source.unsplash.com/800x1000/?leather-jacket",
        "Women Red Dress": "https://source.unsplash.com/800x1000/?red-dress",
        "Women Summer Blouse": "https://source.unsplash.com/800x1000/?blouse",
        "Women Floral Skirt": "https://source.unsplash.com/800x1000/?skirt",
        "Summer Floral Dress": "https://source.unsplash.com/800x1000/?floral-dress",
        "Kids Blue Hoodie": "https://source.unsplash.com/800x1000/?kids-hoodie",
        "Kids Cargo Shorts": "https://source.unsplash.com/800x1000/?cargo-shorts", 
        "Kids Striped Tee": "https://source.unsplash.com/800x1000/?striped-shirt",
        "Kids Denim Jacket": "https://source.unsplash.com/800x1000/?kids-denim-jacket",
    }

    
    # Generic fallbacks by category if exact match not found
    category_fallbacks = {
        "Men": "https://images.unsplash.com/photo-1617137968427-85924c800a22?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "Women": "https://images.unsplash.com/photo-1503342217505-b0815a016253?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        "Kids": "https://images.unsplash.com/photo-1503919545889-aefc3e804f5e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
         "Accessories": "https://images.unsplash.com/photo-1506152983158-b4a74a01c721?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
    }

    print("\nPopulating Products...")
    products = Product.objects.all()
    for product in products:
        print(f"Checking product: {product.name} ({product.category})")
        
        url = product_images.get(product.name)
        if not url:
            # Check if we should use a fallback
            url = category_fallbacks.get(product.category)
            print(f"  -> Using generic fallback for {product.category}")
        else:
            print(f"  -> Found specific URL")

        if url:
            img_blob = download_image(url)
            if img_blob:
                filename = f"{product.name.lower().replace(' ', '_')}_real.jpg"
                product.image.save(filename, File(img_blob), save=True)
                print(f"  -> Updated image for {product.name}")
            else:
                print(f"  -> Failed download for {product.name}")

if __name__ == '__main__':
    populate_collections()
    populate_products()
