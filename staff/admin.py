from django.contrib import admin

from hospital.models import Doctor
from django.utils.html import format_html

from staff.models import Nurse, OtherEmployee

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img style="width:50px; height:50px; border-radius: 50%;" src="{}" />'.format(obj.picture.url))

    image_tag.short_description = 'Image'
    list_display = ("first_name","last_name","age","gender","speciality","experience","availability","working_days","image_tag")
    search_fields = ["first_name","last_name","age","gender","speciality","experience","availability","working_days"]


@admin.register(Nurse)
class NuresAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img style="width:50px; height:50px; border-radius: 50%;" src="{}" />'.format(obj.picture.url))

    image_tag.short_description = 'Image'
    list_display = ("name","age","gender","derpartment","work_time","workdays","image_tag")
    search_fields = ["name","age","gender","derpartment","work_time","workdays"]


@admin.register(OtherEmployee)
class OtherEmployeeAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img style="width:50px; height:50px; border-radius: 50%;" src="{}" />'.format(obj.picture.url))

    image_tag.short_description = 'Image'
    list_display = ("name","age","gender","derpartment","work_time","workdays","type_of_job","image_tag")
    search_fields = ["name","age","gender","derpartment","work_time","type_of_job","workdays"]
