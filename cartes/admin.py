from django.contrib import admin
from .models import Carte,Projet
from .views import selcted_carders

from import_export.admin import ImportExportModelAdmin
from import_export import resources, widgets, fields
from import_export.widgets import ForeignKeyWidget
from django.forms import widgets

class CarteInline(admin.TabularInline):

	model = Carte
	extra = 0
	fields =('image','matricule','noms', 'date_de_naissance','promotion','adresse')
@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('id','nom') 
    search_fields = ( 'id','nom','titre' )   
    fields =   ('nom','front',"back",)
    inlines =[CarteInline,]


def print_to_pdf(modeladmin, request, queryset):    
   return selcted_carders(request,queryset.values())
    
print_to_pdf.short_description = "print pdf"

def  make_printed(modeladmin, request, queryset):
    queryset.update(imprime=True)
make_printed.short_description = "Approuver l'impression"

class CarteResource(resources.ModelResource):

   
    project = fields.Field(
        column_name='projet',
        attribute ='projet',
        widget = ForeignKeyWidget(Projet, 'id')
        
    )
   
    class Meta:
        model   =   Carte
        skip_unchanged = True
        report_skipped = True
        # exclude  =('id')
        import_id_fields  = [ 'projet','matricule', 'noms', 'date_de_naissance', 
                               'promotion', 'adresse', 'image'
                            ]

    def after_save_instance(self, obj: Carte, using_transactions: bool, dry_run: bool,):
            
            super().after_save_instance(obj, using_transactions, dry_run)         
                   

@admin.register(Carte)
class CarteAdmin(ImportExportModelAdmin):
    resource_class = CarteResource
    list_display = ('_image','matricule','noms', 'date_de_naissance','promotion','imprime','projet')
    fields =('projet','image','matricule','noms', 'date_de_naissance','promotion','imprime','adresse')
    list_filter = ('projet','promotion','imprime')
    autocomplete_fields= ['projet',]
    actions = [print_to_pdf,make_printed] 


