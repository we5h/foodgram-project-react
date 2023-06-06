from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.http import HttpResponse
from django.conf import settings


def getpdf(data):
    pdfmetrics.registerFont(TTFont('DejaVuSerif',
                                   settings.BASE_DIR /
                                   'core/fonts/DejaVuSerif.ttf'))
    pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic',
                                   settings.BASE_DIR /
                                   'core/fonts/DejaVuSerif-Italic.ttf'))
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'
    p = canvas.Canvas(response)
    p.setFont("DejaVuSerif", 18)
    str_pos = 750
    p.drawString(50, str_pos, 'Ингридиенты, необходимые для ваших блюд:')
    str_pos -= 50
    for ing in data:
        p.setFont("DejaVuSerif-Italic", 15)
        name = ing['ingredient__name']
        unit = ing['ingredient__measurement_unit']
        amount = ing['ingredient_amount']
        p.drawString(100, str_pos, f'{name} ({unit}) - {amount}')
        str_pos -= 50
    p.setFont("DejaVuSerif-Italic", 10)
    p.drawString(50, str_pos, 'FoodGram App')
    p.showPage()
    p.save()
    return response
