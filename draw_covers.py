import os
import django
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Factory.settings')
django.setup()

from main.models import Product

def draw_tshirt(draw, color, width, height):
    # Draw a T-shirt shape
    # Center x, y
    cx, cy = width // 2, height // 2
    # Body
    body_w, body_h = 200, 300
    # Sleeves
    sleeve_w, sleeve_h = 80, 100
    
    # Coordinates for a simple T-shirt polygon
    # Points: NeckLeft, NeckRight, ShoulderRight, ArmpitRight, HemRight, HemLeft, ArmpitLeft, ShoulderLeft
    
    points = [
        (cx - 50, cy - 150), # Neck Left
        (cx + 50, cy - 150), # Neck Right
        (cx + 120, cy - 100), # Shoulder Right
        (cx + 120, cy - 20),  # Sleeve End Right Top
        (cx + 100, cy - 20),  # Sleeve End Right Bottom
        (cx + 100, cy - 100), # Armpit Right
        (cx + 100, cy + 150), # Hem Right
        (cx - 100, cy + 150), # Hem Left
        (cx - 100, cy - 100), # Armpit Left
        (cx - 100, cy - 20),  # Sleeve End Left Bottom
        (cx - 120, cy - 20),  # Sleeve End Left Top
        (cx - 120, cy - 100), # Shoulder Left
    ]
    draw.polygon(points, fill=color, outline="white")

def draw_dress(draw, color, width, height):
    cx, cy = width // 2, height // 2
    points = [
        (cx - 40, cy - 150), # Top Left
        (cx + 40, cy - 150), # Top Right
        (cx + 60, cy - 50),  # Waist Right
        (cx + 150, cy + 150), # Hem Right
        (cx - 150, cy + 150), # Hem Left
        (cx - 60, cy - 50),  # Waist Left
    ]
    draw.polygon(points, fill=color, outline="white")

def draw_hoodie(draw, color, width, height):
    cx, cy = width // 2, height // 2
    # Similar to tshirt but bulkier and with a "hood" curve
    points = [
        (cx - 60, cy - 160), # Hood Top Left
        (cx + 60, cy - 160), # Hood Top Right
        (cx + 130, cy - 100), # Shoulder Right
        (cx + 130, cy + 50),  # Sleeve Right
        (cx + 100, cy + 50),
        (cx + 110, cy + 150), # Hem Right
        (cx - 110, cy + 150), # Hem Left
        (cx - 100, cy + 50),
        (cx - 130, cy + 50),  # Sleeve Left
        (cx - 130, cy - 100), # Shoulder Left
    ]
    draw.polygon(points, fill=color, outline="white")

def create_artistic_image(product_name, category, bg_color, item_color):
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw specific shape based on category/name
    if "Men" in category or "Shirt" in product_name:
        draw_tshirt(draw, item_color, width, height)
    elif "Women" in category or "Dress" in product_name:
        draw_dress(draw, item_color, width, height)
    elif "Kids" in category or "Hoodie" in product_name:
        draw_hoodie(draw, item_color, width, height)
    else:
        # Fallback circle
        cx, cy = width // 2, height // 2
        draw.ellipse([cx-100, cy-100, cx+100, cy+100], fill=item_color, outline="white")

    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font = ImageFont.load_default()
    
    # Text centered at bottom
    text = product_name
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    draw.text(((width - text_w) / 2, 450), text, fill=(255, 255, 255), font=font)

    blob = BytesIO()
    img.save(blob, 'JPEG')
    return blob

def update_covers():
    # Update specific products to have "Cover" style images
    updates = [
        {"name": "Men Navy T-Shirt", "cat": "Men", "bg": "#ecf0f1", "item": "#2c3e50"},
        {"name": "Women Red Dress", "cat": "Women", "bg": "#fce4ec", "item": "#e91e63"},
        {"name": "Kids Blue Hoodie", "cat": "Kids", "bg": "#e3f2fd", "item": "#2196f3"},
        # Add a few more if they exist
        {"name": "Men Denim Jeans", "cat": "Men", "bg": "#ecf0f1", "item": "#2980b9"},
        {"name": "Women Summer Blouse", "cat": "Women", "bg": "#fff3e0", "item": "#e67e22"},
    ]

    for u in updates:
        print(f"Updating {u['name']}...")
        blob = create_artistic_image(u['name'], u['cat'], u['bg'], u['item'])
        product = Product.objects.filter(name=u['name']).first()
        if product:
             product.image.save(f"{u['name'].replace(' ', '_')}_art.jpg", File(blob), save=True)
             print("Saved.")
        else:
            print("Product not found.")

if __name__ == '__main__':
    update_covers()
