from django.contrib import admin
from .models import (Heart_Care_Basics,Expertize,Appointment,Patient_Profile, Slider, Service, Item, Doctor, Expertize, Faq, Gallery, Prescription,Inpatient)
from django.contrib.auth.models import User
import sys
from import_export.admin import ImportExportModelAdmin

@admin.register(Doctor)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("first_name","address","patients")

    list_filter = ( "first_name","address","mobile")
    search_fields = ("mobile","address","first_name")
    list_per_page = sys.maxsize


    #inlines = [UserinInline]
    #readonly_fields = [ "picture"]

admin.site.register(Appointment)
admin.site.register(Prescription)
admin.site.register(Heart_Care_Basics)
admin.site.register(Slider)
admin.site.register(Service)
admin.site.register(Item)
admin.site.register(Expertize)
admin.site.register(Faq)
admin.site.register(Gallery)
#admin.site.register(Patient_Info_in_Hospital)

class UserinInline(admin.TabularInline):
    model = Doctor
@admin.register(Inpatient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name","age","gender")

    list_filter = ("name", "gender","age")
    date_hierarchy = 'entry_date_time'
    list_per_page = sys.maxsize
    exclude = ("user",)
    #inlines = [UserinInline]
    #order.admin_order_field = '_hero_count'
#admin.site.register(Patient_Profile)

@admin.register(Patient_Profile)
class profileadmin(ImportExportModelAdmin):
    pass