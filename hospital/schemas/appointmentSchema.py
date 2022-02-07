from typing import List
from ninja import Schema
import datetime
from hospital.schemas.patientSchema import PatientProfileSchemaOut 
from hospital.schemas.doctorSchema import DoctorSchemaOut 



class AppointmentSchemaOut(Schema):
    id : str
    patient : PatientProfileSchemaOut
    doctor :DoctorSchemaOut
    symptoms : str
    description : str
    sending_date : datetime.datetime =None
    visit_date : datetime.datetime =None
    status : str = None

class AppointmentSchemaIn(Schema):
    symptoms : str
    description : str
    #sending_date : datetime.datetime = None


class NumberOfAppoinSchema(Schema):
    total_appointment : str
    appointment_done :str
    appointment_upcoming : str