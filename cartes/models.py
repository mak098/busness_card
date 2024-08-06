from django.db import models

from django.utils.safestring import mark_safe
from django.conf import settings

class Projet(models.Model):

    nom= models.CharField(max_length=350, blank=True, verbose_name='nom')       
    front = models.ImageField(upload_to='projet/',verbose_name='front',
            blank=False)   
    back = models.ImageField(upload_to='projet/',verbose_name='back',
            blank=False)
    
    def __str__(self) :
        return  f'{self.nom}'
	  

class Carte(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, blank=True,on_delete=models.PROTECT,related_name='student_created_by' ,verbose_name='Created by' )
    projet = models.ForeignKey(Projet,on_delete=models.PROTECT, related_name='projet')
    matricule = models.CharField(max_length=20,null=True, blank=True, verbose_name='matricule')
    noms= models.CharField(max_length=30, blank=True, verbose_name='noms')
    date_de_naissance= models.CharField(max_length=20,  blank=True,verbose_name='Date de naissance')
    promotion= models.CharField(max_length=30,  blank=True,verbose_name='promotion')
    image = models.ImageField(upload_to='student_images/',default='student_image/student_avatar.png',verbose_name='image etudiant',
         blank=True)
    adresse= models.CharField(max_length=350, null =True, blank=True,verbose_name='adresse')
    # image_url = models.URLField(null=True) 
    # lieu_de_naissance= models.CharField(max_length=350, blank=True, verbose_name='Lieu de naissance')
    # sexe= models.CharField(max_length=350,null =True, blank=True, verbose_name='sexe')
    # faculte= models.CharField(max_length=350,null =True, blank=True, verbose_name='faculte')
    # adresse= models.CharField(max_length=350, null =True, blank=True,verbose_name='adresse')
        
    # date_livraison = models.CharField(max_length=350,  blank=True,verbose_name='Délivrée le')
    # annee_academique = models.CharField(max_length=350, blank=True, verbose_name='année_académique')
    imprime = models.BooleanField(default=False , verbose_name="Imprimé")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _image(self):
        if self.image:
            return mark_safe('<img src="{}" width="100"/>'.format(self.image.url))
        else:
            return mark_safe('<img src="static/avatar.png" width="100"/>')
            # return '(no picture)'
    _image.short_description = 'Image Etudiant'
    _image.allow_tags = True
