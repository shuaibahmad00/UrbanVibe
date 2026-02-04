import os
import django
import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Factory.settings')
django.setup()

from main.models import Product

def create_product_image(text, color, width=600, height=800):
    img = Image.new('RGB', (width, height), color=color)
    d = ImageDraw.Draw(img)
    
    # Draw a "border"
    d.rectangle([10, 10, width-10, height-10], outline="white", width=5)
    
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw Text centered
    text_bbox = d.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) / 2
    y = (height - text_height) / 2
    
    d.text((x, y), text, fill=(255, 255, 255), font=font)
    
    blob = BytesIO()
    img.save(blob, 'JPEG')
    return blob

def populate():
    products_data = [
        # Men
        {'name': 'Men Navy T-Shirt', 'category': 'Men', 'price': 29.99, 'color': '#34495e', 'desc': 'Comfortable cotton t-shirt.'},
        {'name': 'Men Denim Jeans', 'category': 'Men', 'price': 59.99, 'color': '#2980b9', 'desc': 'Classic straight fit jeans.'},
        {'name': 'Men Leather Jacket', 'category': 'Men', 'price': 129.99, 'color': '#2c3e50', 'desc': 'Stylish faux leather jacket.'},
        
        # Women
        {'name': 'Women Red Dress', 'category': 'Women', 'price': 79.99, 'color': '#c0392b', 'desc': 'Elegant red evening dress.'},
        {'name': 'Women Summer Blouse', 'category': 'Women', 'price': 39.99, 'color': '#e67e22', 'desc': 'Light and airy blouse.'},
        {'name': 'Women Floral Skirt', 'category': 'Women', 'price': 49.99, 'color': '#8e44ad', 'desc': 'Beautiful floral pattern skirt.'},
        
        # Kids
        {'name': 'Kids Blue Hoodie', 'category': 'Kids', 'price': 34.99, 'color': '#3498db', 'desc': 'Warm and cozy hoodie.'},
        {'name': 'Kids Cargo Shorts', 'category': 'Kids', 'price': 24.99, 'color': '#27ae60', 'desc': 'Durable shorts for play.'},
        {'name': 'Kids Striped Tee', 'category': 'Kids', 'price': 19.99, 'color': '#f1c40f', 'desc': 'Fun striped t-shirt.'},
    ]

    for p in products_data:
        if not Product.objects.filter(name=p['name']).exists():
            print(f"Creating {p['name']}...")
            blob = create_product_image(p['name'], p['color'])
            product = Product(
                name=p['name'],
                price=p['price'],
                description=p['desc'],
                category=p['category']
            )
            filename = f"{p['name'].lower().replace(' ', '_')}.jpg"
            product.image.save(filename, File(blob), save=True)
            print(f"Saved {p['name']}")
        else:
            print(f"{p['name']} already exists.")

if __name__ == '__main__':
    populate()
