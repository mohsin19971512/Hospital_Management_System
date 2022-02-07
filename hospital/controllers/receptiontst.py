from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from hospital.models import Doctor
from hospital.schemas.appointmentSchema import AppointmentSchemaIn,AppointmentSchemaOut,NumberOfAppoinSchema
from hospital.schemas.doctorSchema import DoctorSchemaIn,DoctorSchemaOut
from hospital.schemas.patientSchema import PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, Patient_Profile
from account.schemas import AccountCreate,AuthOut
from account.authorization import GlobalAuth, get_tokens_for_user

from django.utils import timezone
User = get_user_model()

receptiontst = Router(tags=['receptiontst'])


# create Appointement endpoints
#-----------------------------------------------------------------------------------------
# Add Appointement from receptiontst interface
@receptiontst.post('add_appointment/', response={200:MessageOut})
def add_appointment(request,appointment_in:AppointmentSchemaIn,patient_id:str,doctor_id:str):
    patient = get_object_or_404(Patient_Profile,pk=patient_id)
    doctor = get_object_or_404(Doctor,pk=doctor_id)
    appointment = Appointment.objects.create(**appointment_in.dict(),doctor=doctor,patient=patient)
    appointment.save()

    return 200 ,{'message':'appointment created successfully'}

# receptiontst can accept or delete appointments requests 
@receptiontst.post('receptiontst_add_date/{appointment_id}', response={200:MessageOut})
def  add_date_from_receptionts(request,appointment_id:str,date:datetime):
    appointment = get_object_or_404(Appointment,pk=appointment_id)
    appointment.visit_date = date
    appointment.status = "pending"
    appointment.save()
    return 200 ,{'message':'added interview date successfully'}


#---------------------------------------------------------------------------------------------
# get appointments endpiont

# Return all appointments in receptiontst interface
@receptiontst.get('get_all_appointments/', response={200:List[AppointmentSchemaOut]})
def get_all_appointments(request):
    appintement = Appointment.objects.filter(doctor = get_object_or_404(Doctor,pk=10)).select_related("doctor","patient")
    for i in appintement :
        if i.visit_date :
            if i.visit_date <timezone.now():
                i.status = "completed"
                i.save()
    return 200 ,appintement



# return (total_appointment,appointment_done,appointment_upcoming)
@receptiontst.get('number_of_appointments/', response={200:NumberOfAppoinSchema})
def number_of_appointments(request):

    return 200 ,{
        "total_appointment":Appointment.objects.all().count(),
        "appointment_done" : Appointment.objects.filter(status="completed").count(),
        "appointment_upcoming" : Appointment.objects.filter(status="pending").count(),
        }

#------------------------------------------------------------------------------------------

# add doctor from receptiontst interface
@receptiontst.post('add_doctor/', response={ 400: MessageOut,201: AuthOut})
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
@receptiontst.post('add_patient/', response={ 400: MessageOut,201: AuthOut})
def add_patient(request,patient_in:PatientProfileSchemaIn,user_in:AccountCreate):
        
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
            type = "patient"
        )

        patient = Patient_Profile.objects.create(user = new_user,**patient_in.dict())
        patient.save()
        token = get_tokens_for_user(new_user)
        return 201, {
            'token': token,
            'account': new_user,
        }

    return 400, {'message': 'User already registered!'}








@receptiontst.get('get_all_doctors/', response={200:List[DoctorSchemaOut]})
def get_all_doctors(request):

    doctor = Doctor.objects.all()

    return 200,doctor


@receptiontst.get('get_all_patients/', response={200:List[PatientProfileSchemaOut]})
def get_all_patients(request):
    patient = Patient_Profile.objects.all()

    return 200,patient


