from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from hospital.models import AppointmentFromReceptiontst, Doctor, Inpatient
from hospital.schemas.appointmentSchema import AppointmentFormReceptiontstIn, AppointmentFormReceptiontstOut, AppointmentSchemaIn,AppointmentSchemaOut,NumberOfAppoinSchema
from hospital.schemas.doctorSchema import DoctorSchemaIn,DoctorSchemaOut
from hospital.schemas.patientSchema import InPatientProfileSchemaIn, InPatientProfileSchemaOut, PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, OutPatients
from account.schemas import AccountCreate,AuthOut
from account.authorization import GlobalAuth, get_tokens_for_user

from django.utils import timezone
User = get_user_model()

receptiontst = Router(tags=['receptiontst'])


# create Appointement endpoints
#-----------------------------------------------------------------------------------------
# Add Appointement from receptiontst interface
@receptiontst.post('add-appointment',auth = GlobalAuth() ,response={200:MessageOut,404:MessageOut})
def add_appointment(request,appointment_in:AppointmentFormReceptiontstIn,doctor_id:str):
    try : 
        doctor = get_object_or_404(Doctor,pk=doctor_id)
    except :
        return 200 ,{'message':'doctor Does Not Exist'}

    appointment = AppointmentFromReceptiontst.objects.create(**appointment_in.dict(),doctor=doctor)
    appointment.save()

    return 200 ,{'message':'appointment created successfully'}

@receptiontst.put('update-appointment',auth = GlobalAuth(), response={200:MessageOut})
def update_appointment(request,id:str,appointment_in:AppointmentFormReceptiontstIn):
    appointment = get_object_or_404(AppointmentFromReceptiontst,pk = id)
    for attr, value in appointment_in.dict().items():
        setattr(appointment, attr, value)
    appointment.save()
    return 200 ,{'message':'appointment Updated successfully'}

@receptiontst.delete('delete-appointment/{id}',auth = GlobalAuth(), response={200:MessageOut})
def delete_appointment(request,id:str):
    appointment = get_object_or_404(AppointmentFromReceptiontst,pk = id)
    appointment.delete()
    return 200 ,{'message':'appointment Deleted successfully'}

# receptiontst can accept or delete appointments requests 
@receptiontst.post('receptiontst-add-date/{appointment_id}',auth = GlobalAuth(), response={200:MessageOut})
def  add_date_from_receptionts(request,appointment_id:str,date:datetime):
    appointment = get_object_or_404(Appointment,pk=appointment_id)
    appointment.visit_date = date
    appointment.status = "pending"
    appointment.save()
    return 200 ,{'message':'added interview date successfully'}


#---------------------------------------------------------------------------------------------
# get appointments endpiont

# Return all appointments in receptiontst interface
@receptiontst.get('get_all_appointments/',auth = GlobalAuth(), response={200:List[AppointmentSchemaOut]})
def get_all_appointments(request):
    appintement = Appointment.objects.all().select_related("doctor","patient")
    for i in appintement :
        if i.visit_date :
            if i.visit_date <timezone.now():
                i.status = "completed"
                i.save()
    return 200 ,appintement


@receptiontst.get('get-all-appointments-added-by-receptiontst',auth = GlobalAuth(), response={200:List[AppointmentFormReceptiontstOut]})
def get_all_appointments_added_by_receptiontst(request):
    appintement = AppointmentFromReceptiontst.objects.all().select_related("doctor")
    for i in appintement :
        if i.visit_date :
            if i.visit_date <timezone.now():
                i.status = "completed"
                i.save()
    return 200 ,appintement

# return (total_appointment,appointment_done,appointment_upcoming)
@receptiontst.get('number-of-appointments', auth = GlobalAuth(),response={200:NumberOfAppoinSchema})
def number_of_appointments(request):

    return 200 ,{
        "total_appointment":Appointment.objects.all().count(),
        "appointment_done" : Appointment.objects.filter(status="completed").count(),
        "appointment_upcoming" : Appointment.objects.filter(status="pending").count(),
        }

#------------------------------------------------------------------------------------------

# add doctor from receptiontst interface
@receptiontst.post('add-doctor',auth = GlobalAuth(), response={ 400: MessageOut,201: AuthOut})
def add_doctor(request,doctor_in:DoctorSchemaIn,user_in:AccountCreate):
        
    if user_in.password1 != user_in.password2:
        return 400, {'message': 'Passwords do not match!'}

    try:
        User.objects.get(email=user_in.email)
    except User.DoesNotExist:
        new_user = User.objects.create_user(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            phone_number = user_in.phone_number,
            email=user_in.email,
            password=user_in.password1,
            type = "doctor"
        )

        doctor = Doctor.objects.create(user = new_user,**doctor_in.dict())
        doctor.save()
        token = get_tokens_for_user(new_user)
        return 201, {
            'token': token,
            'account': new_user,
        }

    return 400, {'message': 'User already registered!'}



# add patient from receptiontst interface
@receptiontst.post('add-inpatient',auth = GlobalAuth(), response={ 400: MessageOut,201: AuthOut})
def add_inpatient(request,Inpatient_in:InPatientProfileSchemaIn):
        
    patient = Inpatient.objects.create(**Inpatient_in.dict())
    patient.save()

    return 200, {'message': 'Inpatient created successfully'}




@receptiontst.get('get-all-doctors', response={200:List[DoctorSchemaOut]})
def get_all_doctors(request):

    doctor = Doctor.objects.all()

    return 200,doctor


@receptiontst.get('get-all-outpatients',auth = GlobalAuth(), response={200:List[PatientProfileSchemaOut]})
def get_all_outpatients(request):
    patient = OutPatients.objects.all()

    return 200,patient

@receptiontst.get('get-all-inpatients/', auth = GlobalAuth(),response={200:List[InPatientProfileSchemaOut]})
def get_all_inpatients(request):
    patient = Inpatient.objects.all().select_related('doctor')

    return 200,patient

