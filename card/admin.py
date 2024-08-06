from django.contrib import admin
from .models import Template,Contact,Dealer,SocialMedia
from .card_report import selected_cards,isc_model,public_model,modernexus_model
from .card_report_primary import modernexus_primary

def print_to_pdf(modeladmin, request, queryset):    
   return selected_cards(request,queryset.values())
print_to_pdf.short_description = "print pdf"

def print_isc_to_pdf(modeladmin, request, queryset):    
   return isc_model(request,queryset.values())
print_isc_to_pdf.short_description = "ISC"

def print_public_to_pdf(modeladmin, request, queryset):    
   return public_model(request,queryset.values())
print_public_to_pdf.short_description = "Public"

def print_modernexus_to_pdf(modeladmin, request, queryset):    
   return modernexus_model(request,queryset.values())
print_modernexus_to_pdf.short_description = "modernexus orange"

def print_modernexus_primary_to_pdf(modeladmin, request, queryset):    
   return modernexus_primary(request,queryset.values())
print_modernexus_primary_to_pdf.short_description = "modernexus-primary"


class SocialInline(admin.TabularInline):

	model = SocialMedia
	extra = 0
     
@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display =['name','_front','_back']

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display =['name','phone','email']

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['key','value']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display =['_image','name','phone_1','email_1']
    list_filter =['is_print','dealer__name','template__name']

    fieldsets = (
        ("membership", {
            'fields': (('template'),'dealer'),
        }),
        ('Personal info', {
            'fields': (('name'),'image'),
        }),
        ('Phone number', {
            'fields': (('phone_1', 'phone_2'), 'phone_3'),
        }),
        
        ('Email', {
            'fields': ('email_1', 'email_2'),
        }),
        ('Organisation info', {
            'fields': (('organisation', 'web_site'),('servise','function')),
        }),
        ('Domicil', {
            'fields': ('domicile', ),
        })
    )
    inlines =(SocialInline,)
    actions = [print_modernexus_to_pdf,print_to_pdf,print_isc_to_pdf,print_public_to_pdf,print_modernexus_primary_to_pdf]

    def save_model(self, request, obj, form, change):
        obj.qr_information = f"name: "+obj.name+" phone number: "+obj.phone_1+" email: "+obj.email_1
        obj.save()
	