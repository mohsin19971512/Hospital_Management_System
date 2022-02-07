from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from ninja import NinjaAPI
from django.urls import path
from account.views import account_controller
from hospital.controllers.doctor import doctor
from hospital.controllers.patient import patient
from hospital.controllers.receptiontst import receptiontst


api = NinjaAPI(
    version='1.0.0',
    title='Hospital API v1',
    description='API documentation',
)
api.add_router('doctor', doctor)
api.add_router('patient', patient)
api.add_router('receptiontst', receptiontst)
api.add_router('auth', account_controller)


admin.site.site_header = "Hospital Manager"
admin.site.site_title = "UMSRA Admin Portal"
admin.site.index_title = "Hospital Managment System"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
