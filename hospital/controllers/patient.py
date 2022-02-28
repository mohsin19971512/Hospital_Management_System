from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List
from account.authorization import GlobalAuth
from ninja import Router
from hospital.models import Doctor, Prescription
from hospital.schemas.appointmentSchema import AppointmentSchemaIn,AppointmentSchemaOut,NumberOfAppoinSchema
from hospital.schemas.doctorSchema import PrescriptionSchemaOut
from hospital.schemas.patientSchema import PatientProfileSchemaIn,PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, OutPatients
from django.utils import timezone
User = get_user_model()

patient = Router(tags=['patient'])



# update profile
@patient.put('update-profile',auth=GlobalAuth(), response={200:MessageOut,404:MessageOut})
def update_profile(request,profile_in:PatientProfileSchemaIn):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
    except:
        return 404, {'message': 'User does not exist'}

    profile = get_object_or_404(OutPatients,user = user)
    for attr, value in profile_in.dict().items():
        setattr(profile, attr, value)
    profile.save()

    return 200 ,{'message':'Profile Updated successfully'}


# view profile
@patient.get('OutPatient-profile-info',auth=GlobalAuth(), response={200:PatientProfileSchemaOut,404:MessageOut})
def patient_profile(request):
    try:
        user = User.objects.get(id=request.auth['pk'])
        try :
            patient = OutPatients.objects.get(user = user)
        except User.DoesNotExist:
            return 404, {'message': 'Profile does not exist'}
    except User.DoesNotExist:
        return 404, {'message': 'User does not exist'}
    except :
        return 404, {'message': 'Missing token'}
    return 200 ,patient


# Request Appointement 
@patient.post('patient-add-appointment/',auth=GlobalAuth(), response={201:MessageOut,404:MessageOut})
def patient_add_appointment(request,appointment_in:AppointmentSchemaIn,doctor_id:str):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
        try :
            doctor = get_object_or_404(Doctor,pk=doctor_id)
        except:
            return 404, {'message': 'doctor does not exist'}
    except:
        return 404, {'message': 'User does not exist'}

    patient = get_object_or_404(OutPatients,user=user)
    appointment = Appointment.objects.create(**appointment_in.dict(),sending_date=timezone.now(),status = "requested",doctor=doctor,patient=patient)
    appointment.save()

    return 201 ,{'message':'appointment created successfully'}


#---------------------------------------------------------------------------------------------
# get appointments endpiont
# Return all appointments 
@patient.get('patient-appointments',auth=GlobalAuth(), response={200:List[AppointmentSchemaOut],404:MessageOut})
def patient_appointments(request):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
        outpatient = OutPatients.objects.get(user = user)
        appointment = Appointment.objects.filter(patient=outpatient)
    except:
        return 404, {'message': 'token missing'}
    return 200 ,appointment


    


# return (total_appointment,appointment_done,appointment_upcoming)
@patient.get('number-of-appointments/',auth=GlobalAuth(), response={200:NumberOfAppoinSchema,404:MessageOut})
def number_of_appointments(request):

    try:
        user = get_object_or_404(User, id=request.auth['pk'])
        outpatient = OutPatients.objects.get(user = user)
    except:
        return 404, {'message': 'User does not exist'}

    total_appointment = Appointment.objects.filter(patient = outpatient).count()
    appointment_done = Appointment.objects.filter(patient = outpatient,status = "completed").count()
    appointment_upcoming = Appointment.objects.filter(patient = outpatient,status = "pending").count()
    return 200 ,{
        "total_appointment":total_appointment,
        "appointment_done" : appointment_done,
        "appointment_upcoming" : appointment_upcoming,
        }

#------------------------------------------------------------------------------------------


@patient.get('get-prescriptions',auth=GlobalAuth(), response={200:List[PrescriptionSchemaOut],404:MessageOut})
def get_prescriptions(request):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
        outpatient = OutPatients.objects.get(user = user)
    except:
        return 404, {'message': 'User does not exist'}

    prescription = Prescription.objects.filter(patient = outpatient)
    return 200 , prescription


