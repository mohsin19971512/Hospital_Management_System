from typing import List
from uuid import UUID
from xmlrpc.client import boolean
from ninja import Schema
from account.schemas import AccountOut
from hospital.schemas.doctorSchema import DoctorSchemaOut

from pydantic import UUID4

class PatientProfileSchemaOut(Schema):
    pk : UUID4
    first_name : str = None
    last_name : str = None
    address : str = None
    phone_number : str = None
    profile_pic : str = None

class PatientProfileSchemaIn(Schema):
    first_name : str = None
    last_name : str = None
    address : str = None
    phone_number : str = None
    profile_pic : str = None
    
class InPatientProfileSchemaIn(Schema):
    full_name :str = None
    age : str 
    gender : str
    address :str
    problem : str
    phone : str
    
class InPatientProfileSchemaOut(Schema):
    pk : str
    full_name :str = None
    age : str 
    gender : str
    address :str
    problem : str
    phone : str
    