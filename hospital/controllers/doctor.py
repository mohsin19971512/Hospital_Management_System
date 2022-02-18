from datetime import datetime
from pydoc import Doc
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from hospital.models import Doctor, OutPatients
from hospital.schemas.appointmentSchema import AppointmentSchemaOut
from hospital.schemas.doctorSchema import DoctorSchemaIn,DoctorSchemaOut, PrescriptionSchemaIn
from hospital.schemas.patientSchema import PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, Prescription
from account.authorization import GlobalAuth, get_tokens_for_user

User = get_user_model()

doctor = Router(tags=['doctor'])

# update profile
@doctor.put('update-profile',auth = GlobalAuth(), response={200:MessageOut,404:MessageOut})
def update_profile(request,doctor_in:DoctorSchemaIn):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
    except:
        return 404, {'message': 'User does not exist'}
    doctor = get_object_or_404(Doctor,user=user)

    for attr, value in doctor_in.dict().items():
        setattr(doctor, attr, value)
    doctor.save()

    return 200 ,{'message':'Profile Updated successfully'}

# get doctor appointments
@doctor.get('appointments',auth = GlobalAuth(), response={200:List[AppointmentSchemaOut],404:MessageOut})
def doctor_appointments(request):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
    except:
        return 404, {'message': 'User does not exist'}
    doctor = get_object_or_404(Doctor,user=user)
    appointment = Appointment.objects.filter(doctor = doctor)
    return 200,appointment


# Get Patients Under the doctor care
@doctor.get('patients_under_care',auth = GlobalAuth(), response={200:List[PatientProfileSchemaOut],404:MessageOut})
def patients_under_care(request):
    user = get_object_or_404(User, id=request.auth['pk'])
    doctor = get_object_or_404(Doctor,user=user)
    patient_qs = []
    for i in doctor.patients :
        patient_qs.append(i.patients_qs)  
    return 200,patient_qs


@doctor.post('prescription',auth = GlobalAuth(), response={200:MessageOut,404:MessageOut})
def create_prescription(request,patient_id:str,prescription_in:PrescriptionSchemaIn):
    user = get_object_or_404(User, id=request.auth['pk'])
    doctor = get_object_or_404(Doctor,user=user)
    patient = get_object_or_404(OutPatients,pk=patient_id)
    prescription = Prescription.objects.create(patient=patient,doctor=doctor,**prescription_in.dict())
    prescription.save()
    return 200,{'message':"presecription created successfully"}
