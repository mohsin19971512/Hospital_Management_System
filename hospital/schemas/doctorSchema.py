from typing import List
from ninja import Field, Schema
from account.schemas import AccountCreate,AuthOut,AccountOut
import datetime
from pydantic import UUID4, EmailStr



class CreateDoctorSchema(Schema):
    first_name : str = None
    last_name : str = None
    phone_number : str = None
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str
    gender : str
    age : str
    speciality : str
    picture : str = None
    address : str =None
    experience :str
    availability : str
    working_days : str

class UpdateDoctorSchema(Schema):
    first_name : str = None
    last_name : str = None
    gender : str
    age : str
    speciality : str
    picture : str = None
    address : str =None
    phone_number :str = None
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
    phone_number : str
    experience : str
    expertize : List[Expertize] = None
    availability : str
    working_days : str

class PrescriptionSchemaIn(Schema):
    prescribe : str
    symptoms : str


class ProfileSchemaOut(Schema):
    pk : UUID4
    first_name : str = None
    last_name : str = None
    address : str = None
    phone_number : str = None
    profile_pic : str = None

class PrescriptionSchemaOut(Schema):
    pk:UUID4
    prescribe : str
    symptoms : str
    patient : ProfileSchemaOut
    doctor : DoctorSchemaOut
    created_date : datetime.datetime

