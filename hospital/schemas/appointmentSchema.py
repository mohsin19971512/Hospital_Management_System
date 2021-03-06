from typing import List
from ninja import Schema
from pydantic import UUID4

import datetime
from hospital.schemas.patientSchema import PatientProfileSchemaOut 
from hospital.schemas.doctorSchema import DoctorSchemaOut 



class AppointmentSchemaOut(Schema):
    id : UUID4 = None
    patient : PatientProfileSchemaOut
    doctor :DoctorSchemaOut
    symptoms : str 
    description : str 
    sending_date : datetime.datetime =None
    visit_date : datetime.datetime =None
    status : str 

class AppointmentSchemaIn(Schema):
    symptoms : str
    description : str
    #sending_date : datetime.datetime = None

class AppointmentFormReceptiontstIn(Schema):
    full_name : str 
    symptoms : str
    description : str
    visit_date : datetime.datetime
    status : str

class AppointmentFormReceptiontstOut(Schema):
    pk : UUID4 = None
    full_name : str  
    doctor :DoctorSchemaOut 
    symptoms : str 
    description : str = None
    visit_date : datetime.datetime = None
    status : str




class NumberOfAppoinSchema(Schema):
    total_appointment : str = None
    appointment_done :str = None
    appointment_upcoming : str = None
    admitted_today :str  = None
    doctors : str = None
    inpatients : str =  None
    outpatients : str  = None





"""

class AppointementsForToday(Schema):
    #inappoint : List[AppointmentFormReceptiontstOut]
    AppointmentSchemaOut : List[AppointmentSchemaOut]


"""