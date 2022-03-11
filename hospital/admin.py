from django.contrib import admin

from .models import (Contact,InpatientAppointments,Heart_Care_Basics,Appointment, Medicine,OutPatients, Room_Allotments, Slider, Service, Item, Faq, Gallery, Prescription,Inpatient, Surgery)
from django.contrib.auth.models import User
import sys
from import_export.admin import ImportExportModelAdmin

from django.utils.html import format_html



@admin.register(Appointment)
class Appointmentadmin(admin.ModelAdmin):
    list_display = ("patient","doctor","symptoms","description","sending_date","visit_date","status")
    search_fields = ["patient__first_name","doctor__first_name","symptoms","description","sending_date","visit_date","status"]
    list_filter = ("status",)



@admin.register(Contact)
class Contactadmin(admin.ModelAdmin):
    list_display = ("name","phone_number","subject","created")
    

@admin.register(InpatientAppointments)
class InpatientAppointmentsdmin(admin.ModelAdmin):
    list_display = ("full_name","doctor","symptoms","description","visit_date","status")
    search_fields = ["full_name","doctor__first_name","symptoms","description","visit_date","status"]
    list_filter = ("status",)





@admin.register(Prescription)
class Prescriptionadmin(admin.ModelAdmin):
    list_display = ("prescribe","doctor","symptoms","patient","created_date")
    search_fields = ["patient__first_name","doctor__first_name","symptoms","prescribe","created_date"]

@admin.register(OutPatients)
class OutPatientAdmin(admin.ModelAdmin):
    def picture(self, obj):
        return format_html('<img style="width:50px; height:50px; border-radius: 50%;" src="{}" />'.format(obj.profile_pic.url))

    picture.short_description = 'picture'

    list_display = ("first_name","last_name","gender","age","address","phone_number","picture")


@admin.register(Room_Allotments)
class Room_Allotmentsadmin(admin.ModelAdmin):
    list_display = ("room_number","room_type","patient_name","allotment_date","discharge_date","doctor_name")
    search_fields = ["patient__first_name","doctor__first_name","symptoms","prescribe","created_date"]


@admin.register(Medicine)
class Medicineadmin(admin.ModelAdmin):
    list_display = ("MEDICINE_NAME","SELLING_PRICE","MANUFACTURE_NAME","UNITARY_PRICE","QUANTITY","EXPIRE_DATE","is_expired")


@admin.register(Surgery)
class Surgeryadmin(admin.ModelAdmin):
    list_display = ("name","age","weight","gender","operation_type","diagnoses","entry_date_time","operation_date_time","doctor_name","nurse")
    #search_fields = ["patient__first_name","doctor__first_name","symptoms","prescribe","created_date"]



admin.site.register(Heart_Care_Basics)

admin.site.register(Slider)
admin.site.register(Service)
admin.site.register(Item)
admin.site.register(Faq)
admin.site.register(Gallery)
#admin.site.register(Patient_Info_in_Hospital)

@admin.register(Inpatient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("full_name","age","gender","address","problem","phone","date_admitted")
    list_filter = ("full_name", "gender","age")
    #date_hierarchy = 'entry_date_time'
    #list_per_page = sys.maxsize
    #exclude = ("user",)
    #inlines = [UserinInline]
    #order.admin_order_field = '_hero_count'
#admin.site.register(OutPatients)








"""
@admin.register(Doctor)
class OriginAdmin(admin.ModelAdmin):
    list_display = ("first_name","address","patients")

    list_filter = ( "first_name","address","phone_number")
    search_fields = ("phone_number","address","first_name")
    list_per_page = sys.maxsize


    #inlines = [UserinInline]
    #readonly_fields = [ "picture"]
"""