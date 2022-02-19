from typing import List
from ninja import Schema
from account.schemas import AccountCreate,AuthOut,AccountOut
import datetime
from pydantic import UUID4


class DoctorSchemaIn(Schema):
    first_name : str
    last_name :str
    gender : str
    age : str
    speciality : str
    picture : str = None
    address : str =None
    mobile :str = None
    experience :str
    availability : str
    working_days : str
    

class Expertize(Schema):
    name : str

class DoctorSchemaOut(Schema):
    pk : UUID4
    first_name : str = None
    last_name : str = None
    speciality : str = None
    picture : str = None
    address : str
    mobile : str
    experience : str
    expertize : List[Expertize] = None
    availability : str
    working_days : str

class PrescriptionSchemaIn(Schema):
    prescription : str
    symptoms : str


class ProfileSchemaOut(Schema):
    pk : str
    user : AccountOut
    first_name : str = None
    last_name : str = None
    address : str = None
    phone_number : str = None
    profile_pic : str = None

class PrescriptionSchemaOut(Schema):
    prescribe : str
    symptoms : str
    patient : ProfileSchemaOut
    doctor : DoctorSchemaOut