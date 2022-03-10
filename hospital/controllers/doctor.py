from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from typing import List
from ninja import Router
from staff.models import Doctor
from hospital.schemas.appointmentSchema import AppointmentSchemaOut
from hospital.schemas.doctorSchema import PrescriptionSchemaOut,UpdateDoctorSchema,DoctorSchemaOut, PrescriptionSchemaIn
from hospital.schemas.patientSchema import PatientProfileSchemaOut
from config.utils.schemas import  MessageOut
from hospital.models import Appointment, Prescription
from account.authorization import GlobalAuth

User = get_user_model()

doctor = Router(tags=['doctor'])



# view profile
@doctor.get('doctor-profile-info',auth=GlobalAuth(), response={200:DoctorSchemaOut,404:MessageOut})
def doctor_profile(request):
    try:
        user = User.objects.get(id=request.auth['pk'])
        try :
            doctor = Doctor.objects.get(user = user)
        except User.DoesNotExist:
            return 404, {'message': 'Profile does not exist'}
    except User.DoesNotExist:
        return 404, {'message': 'User does not exist'}
    except :
        return 404, {'message': 'Missing token'}
    return 200 ,doctor


# update profile
@doctor.put('update-profile',auth = GlobalAuth(), response={200:MessageOut,404:MessageOut})
def update_profile(request,doctor_in:UpdateDoctorSchema):
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
    patient_q = []
    for i in doctor.patients_qs :
        patient_q.append(i.patient)  
    return 200,patient_q

# create prescription
@doctor.post('prescription',auth = GlobalAuth(), response={200:MessageOut,404:MessageOut})
def create_prescription(request,patient_id:str,prescription_in:PrescriptionSchemaIn):
    user = get_object_or_404(User, id=request.auth['pk'])
    doctor = get_object_or_404(Doctor,user=user)
    patient = get_object_or_404(OutPatients,pk=patient_id)
    prescription = Prescription.objects.create(patient=patient,doctor=doctor,**prescription_in.dict())
    prescription.save()
    return 200,{'message':"presecription created successfully"}

#get all prescription
@doctor.get('get-all-prescription',auth = GlobalAuth(), response={200:List[PrescriptionSchemaOut],404:MessageOut})
def get_prescriptions(request):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
        doctor = Doctor.objects.get(user = user)
    except:
        return 404, {'message': 'User does not exist'}

    prescription = Prescription.objects.filter(doctor = doctor)
    return 200 , prescription

# update prescription
@doctor.put('update-prescription/{id}',auth = GlobalAuth(), response={200:PrescriptionSchemaOut,404:MessageOut})
def update_prescription(request,prescription_in:PrescriptionSchemaIn,id:str):
    try:
        user = get_object_or_404(User, id=request.auth['pk'])
    except:
        return 404, {'message': 'User does not exist'}
    doctor = get_object_or_404(Doctor,user=user)
    prescription = get_object_or_404(Prescription,id=id)

    for attr, value in prescription_in.dict().items():
        setattr(prescription, attr, value)
    prescription.save()

    return 200 ,prescription


#delete prescription
@doctor.delete('delete-prescription/{id}',auth = GlobalAuth(), response={200:MessageOut,404:MessageOut})
def delete_prescription(request,id:str):
    prescription = get_object_or_404(Prescription,id=id)
    prescription.delete()

    return 200 ,{'message':'prescription deleted successfully'}