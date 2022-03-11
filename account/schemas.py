from typing import Optional
from pydantic import UUID4
from ninja import Schema
from pydantic import EmailStr, Field



class AccountCreate(Schema):
    first_name : str = None
    last_name : str = None
    phone_number : str = None
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str


class AccountOut(Schema):
    pk :UUID4
    first_name : str = None
    last_name : str = None
    phone_number : str = None
    email: EmailStr


class TokenOut(Schema):
    access: str

class AuthOut(Schema):
    token: TokenOut
    account: AccountOut
    type : str


class SigninSchema(Schema):
    email: EmailStr
    password: str


class AccountUpdate(Schema):
    first_name: str
    last_name: str
    phone_number: Optional[str]
    address1: str
    address2: str
    company_name: str
    company_website: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str


class ContactSchema(Schema):
    name : str 
    phone_number : str
    subject : str

