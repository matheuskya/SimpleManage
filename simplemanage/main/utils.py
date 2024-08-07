from PIL import Image, ImageDraw, ImageFont
from main.models import Cardapio
import os
from django.conf import settings

def generate_menu_image():
    #coletando dados do modelo
    menu_items = Cardapio.objects.filter(state= True)

    #carregar imagem de background
    background_path = os.path.join(settings.BASE_DIR, 'main/menu_image/background_pastel_green.jpg')
    img = Image.open(background_path)

    #criando uma imagem nova de fundo branco
    # img = Image.new("RGB", (800,600), color="white")
    img = img.resize((800, 600))


    d = ImageDraw.Draw(img)

    #pegando fonte ttf
    font_path = os.path.join(settings.BASE_DIR, 'main/fonts/cookie-crisp-font/CookieCrisp-L36ly.ttf')
    font = ImageFont.truetype(font_path, 20)    

    #ajustanto o title para o centro
    title_text = "Cardapio de hoje!"
    title_bbox = d.textbbox((0, 0), title_text, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img.width - title_width) / 2
    title_y = 10
    d.text((title_x, title_y), title_text, fill=(0, 0, 0), font=font)

    y_text = 50
    for item in menu_items:
        text = f"{item.name}: {item.description}"
        d.text((10, y_text), text, fill=(0,0,0), font=font)
        y_text += 40

    #salvar imagem no folder especificado   
    # img.save("main/menu_image/menu_image.png")
    
    return img