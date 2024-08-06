from django.shortcuts import render
import json
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import HttpResponse,HttpResponseRedirect
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from .models import Carte
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

def selcted_carders(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/arial_bold.ttf'))
    
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
        data = Carte.objects.get(id=index['id'])
        data.imprime=True
        data.save()      
        # pdf = canvas.Canvas(data['matricule']+".pdf", pagesize=letter)
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.projet.front),0,0,85.6*mm,54*mm)
        
        try:

            # pdf.drawImage("media/"+str(data.image),20,47,35,42,mask='auto')
            img = Image.open("media/"+str(data.image))
            # Créer une version circulaire de l'image
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            # Convertir l'image en format compatible avec ReportLab
            img_io = ImageReader(img)
            pdf.drawImage(img_io,8,40,60,60,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",20,47,35,42,mask='auto')
        
        pdf.setFillColor(HexColor(0x04496B))
        pdf.setFont('arial',7)
        pdf.drawString(140,70,data.noms.upper())
        pdf.drawString(140,59,data.promotion)
        pdf.drawString(140,48,data.date_de_naissance)
        pdf.drawString(140,37.5,data.adresse)
        
        # footer
        pdf.setFillColor(HexColor(0xffffff))
        pdf.setFont('arial',7)
        matricule = data.matricule
        if matricule is None:
            matricule = "-"
        pdf.drawString(35,12,data.matricule)

        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.projet.back),0,0,85.6*mm,54*mm)

        # qr code
        qr = qrcode.QRCode(
                version=3,
                # error_correction=qrcode.constants.ERROR_CORRECT_H,
                # box_size=5,
                border=1,

                # version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        # border=4,
            )
        qr_data = {
            
        } 
        qr_text =f"inst.  :INBTP, mat. :{matricule}, nom :{data.noms} " 
        qr.add_data(qr_text)
        qr.make(fit=False)
        qr_img = qr.make_image()
        pdf.drawInlineImage(qr_img,130,45,60,60)
        pdf.setFillColor(HexColor(0x04496B))
        pdf.setFont('arial',5)
        pdf.drawString(10,30,"Les autorités tant civiles que militaires sont priées d'apporter leur assistance au porteur de la présente")
        pdf.showPage()
    

    pdf.save()
    

    # return HttpResponseRedirect("http://127.0.0.1:8000/student/student/")
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