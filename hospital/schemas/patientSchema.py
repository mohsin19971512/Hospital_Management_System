from typing import List
from xmlrpc.client import boolean
from ninja import Schema
from account.schemas import AccountOut


class PatientProfileSchemaOut(Schema):
    pk : str
    user : AccountOut
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
    