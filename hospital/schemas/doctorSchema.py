from typing import List
from ninja import Schema
from account.schemas import AccountCreate,AuthOut,AccountOut
import datetime

from hospital.models import Patient_Profile
from hospital.schemas.patientSchema import PatientProfileSchemaOut


class DoctorSchemaIn(Schema):
    first_name : str
    last_name :str
    speciality : str
    picture : str = None
    address : str =None
    mobile :str = None
    details :str
    experience :str
    #expertize = models.ManyToManyField(to='Expertize', related_name='doctors')
    twitter :str
    facebook :str
    instagram :str

class Expertize(Schema):
    name : str

class DoctorSchemaOut(Schema):
    pk : str
    user : AccountOut = None
    first_name : str = None
    last_name : str = None
    speciality : str = None
    picture : str = None
    address : str
    mobile : str
    details : str
    experience : str
    expertize : List[Expertize] = None
    twitter : str = None
    facebook : str = None
    instagram : str = None

class PrescriptionSchemaIn(Schema):
    prescription : str
    symptoms : str


class PrescriptionSchemaOut(Schema):
    prescription : str
    symptoms : str
    patient : PatientProfileSchemaOut
    doctor : DoctorSchemaOut