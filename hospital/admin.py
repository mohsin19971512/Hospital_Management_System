from django.contrib import admin
from .models import (InpatientAppointments,Heart_Care_Basics,Expertize,Appointment,OutPatients, Slider, Service, Item, Doctor, Expertize, Faq, Gallery, Prescription,Inpatient)
from django.contrib.auth.models import User
import sys
from import_export.admin import ImportExportModelAdmin

@admin.register(Doctor)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("first_name","address","patients")

    list_filter = ( "first_name","address","phone_number")
    search_fields = ("phone_number","address","first_name")
    list_per_page = sys.maxsize


    #inlines = [UserinInline]
    #readonly_fields = [ "picture"]

admin.site.register(Appointment)
admin.site.register(InpatientAppointments)

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
    list_display = ("full_name","age","gender")

    list_filter = ("full_name", "gender","age")
    #date_hierarchy = 'entry_date_time'
    #list_per_page = sys.maxsize
    #exclude = ("user",)
    #inlines = [UserinInline]
    #order.admin_order_field = '_hero_count'
#admin.site.register(OutPatients)

@admin.register(OutPatients)
class profileadmin(ImportExportModelAdmin):
    pass