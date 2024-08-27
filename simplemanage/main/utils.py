from PIL import Image, ImageDraw, ImageFont
from main.models import Cardapio
import os
from django.conf import settings
import plotly.graph_objects as go


def generate_menu_image():
    #coletando dados do modelo
    menu_items = Cardapio.objects.filter(state= True)

    #carregar imagem de background
    background_path = os.path.join(settings.BASE_DIR, 'main/menu_image/menu.png')
    img = Image.open(background_path)

    #criando uma imagem nova de fundo branco
    # img = Image.new("RGB", (800,600), color="white")
    # 470,600
    img = img.resize((470, 700))


    d = ImageDraw.Draw(img)

    #pegando fonte ttf
    font_path = os.path.join(settings.BASE_DIR, "main/fonts/aovel-sans-rounded-font/AovelSansRounded-rdDL.ttf")
    font = ImageFont.truetype(font_path, 20)    

    #ajustanto o title para o centro
    title_text = f"Cardapio de hoje!                    - Valor/kg: 51,90"
    title_bbox = d.textbbox((0, 0), title_text, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (img.width - title_width) / 2
    title_y = 140
    d.text((title_x, title_y), title_text, fill=(0, 0, 0), font=font)

    y_text = 190
    for item in menu_items:
        text = f"{item.name}: {item.description}"
        d.text((10, y_text), text, fill=(0,0,0), font=font)
        y_text += 40

    #salvar imagem no folder especificado   
    # img.save("main/menu_image/menu_image.png")
    
    return img

def create_pie_chart():
    labels = ['categoria A', 'categoria B', 'categoria C']
    values = ['50', '30' , '10']
    fig = go.Figure(data = [go.Pie(labels=labels, values = values)])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
        width=400,                      # Set the width
        height=300                      # Set the height
    )
    chart_html = fig.to_html(full_html = False)
    return chart_html