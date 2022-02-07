from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from hospital.models import Doctor
from hospital.schemas.appointmentSchema import AppointmentSchemaIn,AppointmentSchemaOut,NumberOfAppoinSchema
from hospital.schemas.patientSchema import PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, Patient_Profile
from django.utils import timezone
User = get_user_model()

patient = Router(tags=['patient'])



# update profile
@patient.put('update_profile/{id}', response={200:MessageOut})
def update_profile(request,profile_in:PatientProfileSchemaIn,id:str,):
    profile = get_object_or_404(Patient_Profile,id=id)
    for attr, value in profile_in.dict().items():
        setattr(profile, attr, value)
    profile.save()

    return 200 ,{'message':'Profile Updated successfully'}


# view profile
@patient.get('patient_profile/{id}', response={200:PatientProfileSchemaOut})
def patient_profile(request,id:str):
    patient = get_object_or_404(Patient_Profile,pk=id)
    return 200 ,patient


# Request Appointement 
@patient.post('patient_add_appointment/', response={201:MessageOut})
def patient_add_appointment(request,appointment_in:AppointmentSchemaIn,patient_id:str,doctor_id:str):
    patient = get_object_or_404(Patient_Profile,pk=patient_id)
    doctor = get_object_or_404(Doctor,pk=doctor_id)
    appointment = Appointment.objects.create(**appointment_in.dict(),sending_date=timezone.now(),status = "requested",doctor=doctor,patient=patient)
    appointment.save()

    return 201 ,{'message':'appointment created successfully'}


#---------------------------------------------------------------------------------------------
# get appointments endpiont
# Return all appointments 
@patient.get('patient_appointments/{patient_id}', response={200:List[AppointmentSchemaOut]})
def patient_appointments(request,patient_id:str):
    patient = get_object_or_404(Patient_Profile,pk=patient_id)
    appointment = Appointment.objects.filter(patient=patient)
    print(appointment.first().total_appointment)

    return 200 ,appointment


# return (total_appointment,appointment_done,appointment_upcoming)
@patient.get('number_of_appointments/{patient_id}', response={200:NumberOfAppoinSchema})
def number_of_appointments(request,patient_id:str):
    total_appointment = Appointment.objects.filter(patient = patient_id).count()
    appointment_done = Appointment.objects.filter(patient = patient_id,status = "completed").count()
    appointment_upcoming = Appointment.objects.filter(patient = patient_id,status = "pending").count()

    return 200 ,{
        "total_appointment":total_appointment,
        "appointment_done" : appointment_done,
        "appointment_upcoming" : appointment_upcoming,
        }

#------------------------------------------------------------------------------------------



