from django.shortcuts import render
import json
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from .models import Contact
from django.conf import settings
import qrcode
import PIL.Image
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from textwrap import wrap
from datetime import datetime

from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.colors import HexColor
from datetime import datetime
from reportlab.lib.colors import Color

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

style = ParagraphStyle('center pragraph',
            fontName="arial-bold",            
            fontSize =9,
            textColor =Color.hexvala(HexColor(0x59DF2)),          
            leading =10,
            alignment=1,
        )


def modernexus_primary(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/Bauhaus93Regular.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/BAUHS93.ttf'))
    pdfmetrics.registerFont(TTFont('arial-arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('italic', 'static/fonts/BauhausItalic.ttf'))
    
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    date_time_str = date_time.replace('/','-')
    filename_str = date_time_str.replace(',','-')
   
      
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+filename_str+'.pdf'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    for i in obj:       
        index = i
        
        data = Contact.objects.get(id=index['id'])
        data.is_print=True
        
        data.save()
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.front),0,0,85.6*mm,54*mm)      
        

        pdf.setFillColor(HexColor(0x484F57))
        pdf.setFont('arial',9)

        p = Paragraph(data.name.upper(), style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =7, 
            leading =8,
            alignment=1,
            textColor = HexColor(0xffffff)
        ))
        p.wrap(75, 75)        
        p.drawOn(pdf, 10, 132.5)

        p = Paragraph(data.function, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =6, 
            leading =7,
            alignment=1,
            textColor = HexColor(0x1DBED3)
        ))
        y_position = 87.5
        # Obtenir la largeur et la hauteur du paragraphe
        p.wrap(75, 75)
        paragraph_width, paragraph_height = p.wrap(75, 75)
        # Calculer la nouvelle position y après le retour à la ligne
        y_position -= paragraph_height
        # Dessiner le paragraphe à la nouvelle position y
        p.drawOn(pdf, 10, y_position)
                

        pdf.setFillColor(HexColor(0xffffff))
        
        pdf.setFont('arial-arial',6)
        pdf.drawString(130,122,data.phone_1)
        if  data.phone_2 is not None and data.phone_2 is not '-':
            pdf.drawString(130,112,data.phone_2)
        pdf.drawString(130,93,data.email_1)
        if data.email_2 is not None and data.email_2 is not '-':
            pdf.drawString(130,83,data.email_2)
        if data.web_site is not None and data.web_site is not '-':
            pdf.drawString(130,62,data.web_site)


        p = Paragraph(data.domicile, style=ParagraphStyle('center pragraph',
            fontName="arial-arial",            
            fontSize =6, 
            leading =7,
            alignment=0,  
            textColor = HexColor(0xffffff)
        ))
        p.wrap(75,75)
        p.drawOn(pdf,125,10)

        # ===qr code
        # =========
        qr_text = "https://wa.me/"+str(data.phone_1).replace("+", "")
        import segno
        _qrcode = segno.make(qr_text, error='h')
        _img = _qrcode.to_pil(scale=4, dark='orange', data_dark='black',
                   data_light='white')
        pdf.drawInlineImage(_img,31,27,30,30)
        
        try:
            img = Image.open("media/"+str(data.image))
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            img_io = ImageReader(img)
            pdf.drawImage(img_io,28.8,91.5,35.1,35.1,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",71,53,55,55,mask='auto')
        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.back),0,0,85.6*mm,54*mm)        
        pdf.drawInlineImage(_img,114,57,40,40) 
        pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

def circle_image(image):
    # Créer un masque circulaire
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + image.size, fill=255)

    # Appliquer le masque à l'image
    image.putalpha(mask)

    return image