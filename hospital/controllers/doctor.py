from datetime import datetime
from pydoc import Doc
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from hospital.models import Doctor, Patient_Profile
from hospital.schemas.appointmentSchema import AppointmentSchemaOut
from hospital.schemas.doctorSchema import DoctorSchemaIn,DoctorSchemaOut, PrescriptionSchemaIn
from hospital.schemas.patientSchema import PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, Prescription
from account.schemas import AccountCreate,AuthOut
from account.authorization import GlobalAuth, get_tokens_for_user

User = get_user_model()

doctor = Router(tags=['doctor'])

# update profile
@doctor.put('update_profile/{id}', response={200:MessageOut})
def update_profile(request,doctor_in:DoctorSchemaIn,id:str,):
    doctor = get_object_or_404(Doctor,id=id)
    for attr, value in doctor_in.dict().items():
        setattr(doctor, attr, value)
    doctor.save()

    return 200 ,{'message':'Profile Updated successfully'}

# get doctor appointments
@doctor.get('appointments/{doctor_id}', response={200:List[AppointmentSchemaOut]})
def doctor_appointments(request,doctor_id:str):
    appointment = Appointment.objects.filter(doctor = doctor_id)
    return 200,appointment


# Get Patients Under the doctor care
@doctor.get('patients_under_care/{doctor_id}', response={200:List[PatientProfileSchemaOut]})
def patients_under_care(request,doctor_id:str):
    doctor = get_object_or_404(Doctor,pk=doctor_id)
    patient_qs = []
    for i in doctor.patients :
        patient_qs.append(i.patients_qs)  
    return 200,patient_qs


@doctor.post('prescription/', response={200:MessageOut})
def create_prescription(request,doctor_id:str,patient_id:str,prescription_in:PrescriptionSchemaIn):
    doctor = get_object_or_404(Doctor,pk=doctor_id)
    patient = get_object_or_404(Patient_Profile,pk=patient_id)
    prescription = Prescription.objects.create(patient=patient,doctor=doctor,**prescription_in.dict())
    prescription.save()

    return 200,{'message':"presecription created successfully"}
