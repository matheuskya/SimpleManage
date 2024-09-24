from PIL import Image, ImageDraw, ImageFont
from main.models import Cardapio, RegistroFinanceiro
import os
from django.conf import settings
import plotly.graph_objects as go
from django.db.models import Sum
from typing import Union
from datetime import datetime, timedelta
from django.utils.timezone import now

def generate_menu_image(date: str):
    #coletando dados do modelo
    menu_items = Cardapio.objects.filter(state= True)

    #formatar a data
    date = f"{date[8:10]}/{date[5:7]}/{date[0:4]}"

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
    title_text = f"Cardapio de {date}                    - Valor/kg: 51,90"
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

def create_pie_chart(title: str, category: Union[str, None]):
    labels = ['categoria A', 'categoria B', 'categoria C']
    values = ['50', '30' , '10']
    fig = go.Figure(data = [go.Pie(labels=labels, values = values)])
    fig.update_layout(
        title={
            "x":0.5,
        },
        title_text = f"{title}",
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
        width=400,                      # Set the width
        height=400,                      # Set the height, valor orginal 300
    )
    chart_html = fig.to_html(full_html = False)
    print(category)
    return chart_html

def value_card_registrofinanceiro():
    total = RegistroFinanceiro.objects.filter(state=1).aggregate(Sum('value'))['value__sum']
    return total

def card_clientes_ativos():
    total_active_clients = RegistroFinanceiro.objects.filter(state=1).filter(category="cliente").count()  
    return total_active_clients

def create_registrofinanceiro_chart(title: str):
    category_values=['cliente', 'funcionario', 'custo']
    labels = ['Cliente', 'Funcionario', 'Custos']
    values = [
        RegistroFinanceiro.objects.filter(category=category_values[0], state=1).aggregate(Sum('value'))['value__sum'] or 0,
        RegistroFinanceiro.objects.filter(category=category_values[1], state=1).aggregate(Sum('value'))['value__sum'] or 0,
        RegistroFinanceiro.objects.filter(category=category_values[2], state=1).aggregate(Sum('value'))['value__sum'] or 0,
    ]
    fig = go.Figure(data = [go.Pie(labels=labels, values = values)])
    fig.update_layout(
        title={
            "x":0.5,
        },
        title_text = f"{title}",
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
        width=400,                      # Set the width
        height=400,                      # Set the height, valor orginal 300
    )
    chart_html = fig.to_html(full_html = False)
    return chart_html

def calculate_trend():
    # Get the current date and time
    today = now()
    
    # Define the current period (e.g., current month)
    start_of_current_period = today.replace(day=1)  # Start of current month
    
    # Define the previous period (e.g., previous month)
    start_of_previous_period = (start_of_current_period - timedelta(days=1)).replace(day=1)
    end_of_previous_period = start_of_current_period - timedelta(days=1)  # End of last month

    # Query total costs for the current period
    current_period_costs = RegistroFinanceiro.objects.filter(
        date__gte=start_of_current_period, 
        state=1
    ).aggregate(Sum('value'))['value__sum'] or 0

    # Query total costs for the previous period
    previous_period_costs = RegistroFinanceiro.objects.filter(
        date__range=(start_of_previous_period, end_of_previous_period),
        state=1
    ).aggregate(Sum('value'))['value__sum'] or 0

    # Calculate the trend percentage (growth or decline)
    if previous_period_costs == 0:
        trend = 0 if current_period_costs == 0 else 100  # Avoid division by zero
    else:
        trend = ((current_period_costs - previous_period_costs) / previous_period_costs) * 100

    # Return the trend and a status
    if trend > 0:
        return f"Costs increased by {trend:.2f}%"
    elif trend < 0:
        return f"Costs decreased by {abs(trend):.2f}%"
    else:
        return "No change in costs"