from PIL import Image, ImageDraw, ImageFont
from main.models import Cardapio

def generate_menu_image():
    menu_items = Cardapio.objects.filter(state= True)

    img = Image.new("RGB", (800,600), color="white")
    d = ImageDraw.Draw(img)

    font  = ImageFont.load_default()

    d.text((10,10), "Cardapio de hoje!:", fill=(0,0,0), font=font)

    y_text = 50
    for item in menu_items:
        text = f"{item.name}: {item.description}"
        d.text((10, y_text), text, fill=(0,0,0), font=font)
        y_text += 20

    img.save("main/menu_image/menu_image.png")
    
    return img