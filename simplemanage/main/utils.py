from PIL import Image, ImageDraw, ImageFont
from main.models import Cardapio, RegistroFinanceiro
import os
from django.conf import settings
import plotly.graph_objects as go
import plotly.express as px
from django.db.models import Sum
from typing import Union
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth, ExtractYear
# from django.http import HttpRequest


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

def create_value_card(categoria: str, request):
    if categoria != "":
        if categoria == "cliente":
            total = RegistroFinanceiro.objects.filter(state=1).filter(category=categoria).filter(user=request.user).aggregate(Sum('value'))['value__sum'] or 0
        elif categoria == "funcionario":
            total = RegistroFinanceiro.objects.filter(user=request.user).filter(state=1).filter(category=categoria).aggregate(Sum('value'))['value__sum'] or 0
        elif categoria == "custo":
            total = RegistroFinanceiro.objects.filter(user=request.user).filter(state=1).filter(category=categoria).aggregate(Sum('value'))['value__sum'] or 0
        else:
            total = RegistroFinanceiro.objects.filter(user=request.user).filter(state=1).aggregate(Sum('value'))['value__sum'] or 0
    else:
        total = RegistroFinanceiro.objects.filter(user=request.user).filter(state=1).aggregate(Sum('value'))['value__sum'] or 0
    total = round(float(total),2)
    total = str(total)
    for i in total:
        if i == '.':
            total = total.replace('.', ',')
    # return round(float(total), 2) if total is not None else 0
    return total

def create_active_card(category: str, request):
    total_active_clients = RegistroFinanceiro.objects.filter(user=request.user).filter(state=1).filter(category=category).count()
    return total_active_clients

def create_registrofinanceiro_chart(title: str, request):
    category_values=['cliente', 'funcionario', 'custo']
    labels = ['Cliente', 'Funcionario', 'Custos']
    values = [
        RegistroFinanceiro.objects.filter(user=request.user).filter(category=category_values[0], state=1).aggregate(Sum('value'))['value__sum'] or 0,
        RegistroFinanceiro.objects.filter(user=request.user).filter(category=category_values[1], state=1).aggregate(Sum('value'))['value__sum'] or 0,
        RegistroFinanceiro.objects.filter(user=request.user).filter(category=category_values[2], state=1).aggregate(Sum('value'))['value__sum'] or 0,
    ]
    fig = go.Figure(data = [go.Pie(labels=labels, values = values)])
    fig.update_layout(
        title={
            "x":0.5,
        },
        title_text = f"{title}",
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        # plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
        width=400,                      # Set the width
        height=400,                      # Set the height, valor orginal 300
    )
    chart_html = fig.to_html(full_html = False)

    return chart_html


def create_monthly_expense_chart(request):
    months=['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    records = RegistroFinanceiro.objects.filter(user=request.user).filter(state=True).order_by('created_at')

    records_formatado=[0,0,0,0,0,0,0,0,0,0,0,0]
    #formatando dados para lista
    for i in records:
        index = i.created_at.month - 1
        if i.created_at.month == 1:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 2:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 3:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 4:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 5:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 6:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 7:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 8:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 9:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 10:
            records_formatado[index] = i.value + records_formatado[index]
        elif i.created_at.month == 11:
            records_formatado[index] = i.value + records_formatado[index]

    print(records_formatado)

    fig = go.Figure([go.Bar(x=months, y=records_formatado)])

    fig.update_layout(
                    title_text='Custos / Gastos ao longo do tempo',
                    title={
                        "x":0.5,
                    },
                    # xaxis_title='Data',
                    # yaxis_title='Valor total',
                    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
                    # plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
                    width=400,                      # Set the width
                    height=400,            # Set the height, valor orginal 300
        )

    #
    return fig.to_html(full_html=False)
