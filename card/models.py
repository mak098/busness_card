from django.db import models

from django.utils.safestring import mark_safe
from django.conf import settings

class Dealer (models.Model):
    name = models.CharField(max_length=20, blank=True, verbose_name='name')       
    phone = models.CharField(max_length=20, blank=True, verbose_name='phone')       
    email = models.CharField(max_length=20, blank=True, verbose_name='email')       
    
    def __str__(self) :
        return  f'{self.name}'

class Template(models.Model):

    name = models.CharField(max_length=350, blank=True, verbose_name='name')       
    front = models.ImageField(upload_to='template/',verbose_name='front',
            blank=False)   
    back = models.ImageField(upload_to='template/',verbose_name='back',
            blank=False)
    
    def __str__(self) :
        return  f'{self.name}'
	
    def _front(self):
        if self.front:
            return mark_safe('<img src="{}" width="100"/>'.format(self.front.url))
        else:
            return '(no picture)'
    _front.short_description = 'front image'
    _front.allow_tags = True

    def __str__(self) :
        return  f'{self.name}'
	

    def _back(self):
        if self.back:
            return mark_safe('<img src="{}" width="100"/>'.format(self.back.url))
        else:
            return '(no picture)'
    _back.short_description = 'back image'
    _back.allow_tags = True

class Contact(models.Model):

    name = models.CharField(max_length=50, blank=True, verbose_name='name')       
    phone_1 = models.CharField(max_length=50, blank=True, verbose_name='phone 1')       
    phone_2 = models.CharField(max_length=50, null=True, blank=True, verbose_name='phone 1')       
    phone_3 = models.CharField(max_length=50,null=True, blank=True, verbose_name='phone 1')       
    email_1 = models.CharField(max_length=50, blank=True, verbose_name='email 1')       
    email_2 = models.CharField(max_length=50,null=True,blank=True, verbose_name='email 2')       
    domicile = models.CharField(max_length=100,null=True,default='', blank=True, verbose_name='Domicile')       
    organisation = models.CharField(max_length=256,null=True, blank=True, verbose_name='Organisation')       
    web_site = models.CharField(max_length=50, null=True, blank=True, verbose_name='Web site')       
    servise = models.CharField(max_length=100,null=True, blank=True, verbose_name='Servise')       
    function = models.CharField(max_length=150,null=True, blank=True, verbose_name='Function')       
    image = models.ImageField(upload_to='contact/',verbose_name='image',
            blank=True,null=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='created_by' ,verbose_name='Created by' )
    template = models.ForeignKey(Template,null=True, blank=True,on_delete=models.PROTECT,related_name='card_template' ,verbose_name='Template' )
    dealer = models.ForeignKey(Dealer,null=True, blank=True,on_delete=models.PROTECT,related_name='card_dealer' ,verbose_name='Dealer' )
    is_print = models.BooleanField(default=False)
    print_at = models.DateTimeField(auto_now=True)
    qr_information =models.CharField(max_length=255,null=True,default='-', blank=True, verbose_name='qr code info') 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return  f'{self.name} {self.phone_1} {self.email_1}'
    
    def qr_info(self):
        return f"name:"+self.name+" phone number "+self.phone_1+" email "+self.email_1
    
    def _image(self):
        if self.image:
            return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
        else:
            return mark_safe('<img src="static/avatar.png" width="100"/>')
            # return '(no picture)'
    _image.short_description = 'Image Etudiant'
    _image.allow_tags = True

class SocialMedia(models.Model):
    key = models.CharField(max_length=50, blank=True, verbose_name='key') 
    value = models.CharField(max_length=50, blank=True, verbose_name='value') 
    contact = models.ForeignKey(Contact,null=True, blank=True,on_delete=models.PROTECT,related_name='contact_social' ,verbose_name='Contact' )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) :
        return f'{self.key}: {self.value}'