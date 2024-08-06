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

def selected_cards(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/arial_bold.ttf'))
    pdfmetrics.registerFont(TTFont('italic', 'static/fonts/italic.ttf'))
    
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
        
        try:
            img = Image.open("media/"+str(data.image))
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            img_io = ImageReader(img)
            pdf.drawImage(img_io,27,49,59,59,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",20,47,35,42,mask='auto')

        pdf.setFillColor(HexColor(0x13A89E))
        pdf.setFont('arial',9)
        pdf.drawString(110,120,data.name)

        # p = Paragraph(data.name, style=ParagraphStyle('center pragraph',
        #     fontName="arial",            
        #     fontSize =9.5, 
        #     leading =12,
        #     alignment=0,
        #     textColor = HexColor(0x13A89E)
        # ))
        # p.wrapOn(pdf,155,0)
        # p.drawOn(pdf,105,115)


        pdf.setFont('italic',6.5)
        pdf.drawString(130,98,data.phone_1)
        pdf.drawString(130,85,data.email_1)
        pdf.drawString(130,70,data.web_site)
        pdf.drawString(130,55,data.domicile)

        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.back),0,0,85.6*mm,54*mm)
        # qr code
        qr = qrcode.QRCode(
            version=11,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=1
        )
        qr.add_data(data.web_site)
        
        qr.make(fit=True)
        qr_img = qr.make_image()
        pdf.drawInlineImage(qr_img,100,60,60,60)
        p = Paragraph(data.name, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =13, 
            leading =16,
            alignment=1,
            textColor = HexColor(0xffffff)
            ))
        p.wrapOn(pdf,140,25)
        p.drawOn(pdf,60,28)
        pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

def isc_model(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/arial_bold.ttf'))
    pdfmetrics.registerFont(TTFont('italic', 'static/fonts/italic.ttf'))
    
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
        
        try:
            img = Image.open("media/"+str(data.image))
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            img_io = ImageReader(img)
            pdf.drawImage(img_io,71,49,55,55,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",20,47,35,42,mask='auto')

        pdf.setFillColor(HexColor(0x484F57))
        pdf.setFont('arial',9)
        # pdf.drawString(110,120,data.name)

        p = Paragraph(data.name, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =8, 
            leading =12,
            alignment=0,
            textColor = HexColor(0x484F57)
        ))
        p.wrap(85,100)
        p.drawOn(pdf,155,115)


        pdf.setFont('arial',6.5)

        largeur_texte = pdf.stringWidth(data.function)
        x = letter[0] - largeur_texte - 380
        pdf.drawString(x, 110, data.function) 

        # pdf.drawString(155,110,data.function)
        # pdf.setFont('italic',6.5)

        largeur_texte = pdf.stringWidth(data.phone_1)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x, 75, data.phone_1) 
        # pdf.drawString(160,75,data.phone_1)        
        pdf.drawString(x,63,data.phone_2)
        largeur_texte = pdf.stringWidth(data.email_1)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x,50,data.email_1)

        largeur_texte = pdf.stringWidth(data.web_site)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x,38,data.web_site)
        # pdf.drawString(160,26,data.domicile)
        p = Paragraph(data.domicile, style=ParagraphStyle('center pragraph',
            fontName="italic",            
            fontSize =6.5, 
            leading =8,
            alignment=0,  
            textColor = HexColor(0x484F57)
        ))
        p.wrap(100,100)
        p.drawOn(pdf,160,17)

        # qr code
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=1
        )
        qr.add_data(data.web_site)
        
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color='white', back_color='black')
        pdf.drawInlineImage(qr_img,10,15,30,30)
        

        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.back),0,0,85.6*mm,54*mm)

        pdf.drawImage("static/icons/drc.png",40,95,35,35,mask="auto")
        pdf.drawImage("static/icons/esu.png",95,95,30,35,mask="auto")
        pdf.drawImage("static/icons/heck.png",138,93,37,40,mask="auto")
        
        p = Paragraph(data.servise.upper(), style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =7, 
            leading =9,
            alignment=1,
            textColor = HexColor(0x000000),
            ))
        p.wrapOn(pdf,200,200)
        p.drawOn(pdf,20,46)
        pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

def public_model(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/arial_bold.ttf'))
    pdfmetrics.registerFont(TTFont('italic', 'static/fonts/italic.ttf'))
    
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
        
        try:
            img = Image.open("media/"+str(data.image))
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            img_io = ImageReader(img)
            pdf.drawImage(img_io,71,49,55,55,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",71,49,55,55,mask='auto')

        pdf.setFillColor(HexColor(0x484F57))
        pdf.setFont('arial',9)
        # pdf.drawString(110,120,data.name)

        p = Paragraph(data.name, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =8, 
            leading =12,
            alignment=0,
            textColor = HexColor(0x484F57)
        ))
        p.wrap(85,100)
        p.drawOn(pdf,155,115)


        pdf.setFont('arial',6.5)

        largeur_texte = pdf.stringWidth(data.function)
        x = letter[0] - largeur_texte - 380
        pdf.drawString(x, 110, data.function) 

        # pdf.drawString(155,110,data.function)
        # pdf.setFont('italic',6.5)

        largeur_texte = pdf.stringWidth(data.phone_1)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x, 75, data.phone_1) 
        # pdf.drawString(160,75,data.phone_1)        
        pdf.drawString(x,63,data.phone_2)
        pdf.setFont('arial',5.7)
        largeur_texte = pdf.stringWidth(data.email_1)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x,50,data.email_1)
        pdf.setFont('arial',6.5)
        largeur_texte = pdf.stringWidth(data.web_site)
        x = letter[0] - largeur_texte - 400
        pdf.drawString(x,40,data.web_site)
        largeur_texte = pdf.stringWidth(data.domicile)
        
        largeur_texte = pdf.stringWidth(data.domicile)
        x = letter[0] - largeur_texte - 350
        p = Paragraph(data.domicile, style=ParagraphStyle('center pragraph',
            fontName="italic",            
            fontSize =6.3, 
            leading =8,
            alignment=0,  
            textColor = HexColor(0x484F57)
        ))
        p.wrap(100,100)
        p.drawOn(pdf,120,22)

        # phone = data.phone_1
        # if "+" in data.phone:
        #     phone = phone.replace("+", "")
        qr_text = "https://wa.me/"+str(data.phone_1).replace("+", "")
        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=1
        )
        qr.add_data(qr_text)
        
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color='white', back_color='black')
        pdf.drawInlineImage(qr_img,10,15,30,30)
        

        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.back),0,0,85.6*mm,54*mm)

        qr = qrcode.QRCode(
            version=3,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=5,
            border=1
        )
        qr.add_data(qr_text)
        
        qr.make(fit=True)
        qr_img = qr.make_image()
        pdf.drawInlineImage(qr_img,89,60,60,60)
        
        # p = Paragraph(data.servise.upper(), style=ParagraphStyle('center pragraph',
        #     fontName="arial",            
        #     fontSize =7, 
        #     leading =9,
        #     alignment=1,
        #     textColor = HexColor(0x000000),
        #     ))
        # p.wrapOn(pdf,200,200)
        # p.drawOn(pdf,20,46)
        pdf.showPage()
    pdf.save()
    p = buffer.getvalue()
    buffer.close()
    response.write(p)
    return response

def modernexus_model(request,obj):
    pdfmetrics.registerFont(TTFont('arial', 'static/fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold', 'static/fonts/BAUHS93.ttf'))
    pdfmetrics.registerFont(TTFont('arial-bold-italic', 'static/fonts/BauhausBoldItalic.ttf'))
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
            fontName="arial-bold",            
            fontSize =10, 
            leading =11,
            alignment=0,
            textColor = HexColor(0x484F57)
        ))
        p.wrap(100,100)
        p.drawOn(pdf,10,123)

        p = Paragraph(data.function, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =7.5, 
            leading =7,
            alignment=0,
            textColor = HexColor(0xff6000)
        ))
        # p.wrap(135,135)
        # p.drawOn(pdf,9,110)

        y_position = 119.3
        # Obtenir la largeur et la hauteur du paragraphe
        p.wrap(90, 90)
        paragraph_width, paragraph_height = p.wrap(90, 90)
        # Calculer la nouvelle position y après le retour à la ligne
        y_position -= paragraph_height
        # Dessiner le paragraphe à la nouvelle position y
        p.drawOn(pdf, 9, y_position)
                

        pdf.setFillColor(HexColor(0x484F57))
        pdf.setFont('arial',8)
        
        pdf.drawImage("static/icon2/phone.png",10,38,10,10,mask='auto')
        pdf.drawImage("static/icon2/email.png",10,21,10,10,mask='auto')
        pdf.drawImage("static/icon2/website.png",10,5,10,10,mask='auto')
        pdf.setFont('arial',6.5)
        pdf.drawString(22,43,data.phone_1)
        if data.phone_2 is not None and data.phone_2 is not '-':
            pdf.drawString(22,35,data.phone_2)
        pdf.drawString(22,25,data.email_1)
        if data.email_2 is not None and data.email_2 is not '-':
            pdf.drawString(22,17,data.email_2)
        if data.web_site is not None and data.web_site is not '-':
            pdf.drawString(22,9,data.web_site)


        p = Paragraph(data.domicile, style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =7, 
            leading =8,
            alignment=0,  
            textColor = HexColor(0x484F57)
        ))
        y_position = 55
        # Obtenir la largeur et la hauteur du paragraphe
        p.wrap(75, 75)
        paragraph_width, paragraph_height = p.wrap(75, 75)
        # Calculer la nouvelle position y après le retour à la ligne
        y_position -= paragraph_height
        # Dessiner le paragraphe à la nouvelle position y
        p.drawOn(pdf, 150, y_position)

        # ===qr code
        # =========
        qr_text = "https://wa.me/"+str(data.phone_1).replace("+", "")
        import segno
        _qrcode = segno.make(qr_text, error='h')
        _img = _qrcode.to_pil(scale=4, dark='orange', data_dark='black',
                   data_light='white')
        pdf.drawInlineImage(_img,165,80,62,62)
        
        try:
            img = Image.open("media/"+str(data.image))
            img = circle_image(img)
            from reportlab.lib.utils import ImageReader
            img_io = ImageReader(img)
            pdf.drawImage(img_io,22.5,58,40,40,mask='auto')
        except:
            pdf.drawImage("./static/avatar.png",71,53,55,55,mask='auto')
        pdf.showPage()
    
        pdf.setPageSize( (85.6*mm,54*mm) )
        pdf.drawInlineImage("media/"+str(data.template.back),0,0,85.6*mm,54*mm) 
        p = Paragraph(data.organisation.upper(), style=ParagraphStyle('center pragraph',
            fontName="arial-bold",            
            fontSize =10, 
            leading =11,
            alignment=1,
            textColor = HexColor(0x484F57)
        ))
        # p.wrap(135,135)
        # p.drawOn(pdf,9,110)

        y_position = 140
        # Obtenir la largeur et la hauteur du paragraphe
        p.wrap(200, 200)
        paragraph_width, paragraph_height = p.wrap(200, 200)
        # Calculer la nouvelle position y après le retour à la ligne
        y_position -= paragraph_height
        # Dessiner le paragraphe à la nouvelle position y
        p.drawOn(pdf, 20, y_position)

        p = Paragraph(data.servise.upper(), style=ParagraphStyle('center pragraph',
            fontName="arial",            
            fontSize =8, 
            leading =8,
            alignment=1,
            textColor = HexColor(0x484F57)
        ))
        # p.wrap(135,135)
        # p.drawOn(pdf,9,110)

        y_position = 50
        # Obtenir la largeur et la hauteur du paragraphe
        p.wrap(200, 200)
        paragraph_width, paragraph_height = p.wrap(200, 200)
        # Calculer la nouvelle position y après le retour à la ligne
        y_position -= paragraph_height
        # Dessiner le paragraphe à la nouvelle position y
        p.drawOn(pdf, 20, y_position)

        pdf.drawInlineImage(_img,89,54,60,60) 
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