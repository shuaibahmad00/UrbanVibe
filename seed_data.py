import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Factory.settings')
django.setup()

from main.models import Product
from django.core.files import File
from io import BytesIO

def create_placeholder_image(text, color):
    img = Image.new('RGB', (800, 600), color=color)
    d = ImageDraw.Draw(img)
    # Try to load a default font, otherwise use default
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position (rough centering)
    # precise centering requires font metrics which varies, simple approximation is fine
    d.text((250, 250), text, fill=(255, 255, 255), font=font)
    
    blob = BytesIO()
    img.save(blob, 'JPEG')
    return blob

def seed_products():
    products = [
        {
            'name': 'Classic Men Suit',
            'price': 199.99,
            'description': 'A timeless classic for the modern man.',
            'category': 'Men',
            'color': '#2c3e50',
            'filename': 'men_collection.jpg'
        },
        {
            'name': 'Summer Floral Dress',
            'price': 89.99,
            'description': 'Light and breezy for the summer season.',
            'category': 'Women',
            'color': '#e91e63',
            'filename': 'women_collection.jpg'
        },
        {
            'name': 'Kids Denim Jacket',
            'price': 45.99,
            'description': 'Durable and stylish for active kids.',
            'category': 'Kids',
            'color': '#f1c40f',
            'filename': 'kids_collection.jpg'
        }
    ]

    for p_data in products:
        if not Product.objects.filter(name=p_data['name']).exists():
            print(f"Creating {p_data['name']}...")
            blob = create_placeholder_image(p_data['category'] + " Collection", p_data['color'])
            product = Product(
                name=p_data['name'],
                price=p_data['price'],
                description=p_data['description'],
                category=p_data['category']
            )
            product.image.save(p_data['filename'], File(blob), save=True)
            print(f"Saved {p_data['name']}")
        else:
            print(f"{p_data['name']} already exists")

if __name__ == '__main__':
    seed_products()
