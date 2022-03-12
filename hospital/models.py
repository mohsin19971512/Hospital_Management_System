import email
from django.db import models
from django.contrib.auth import get_user_model

from config.utils.models import Entity
User = get_user_model()
from django.utils import timezone
from datetime import datetime
from staff.models import Doctor

class OutPatients(Entity):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,verbose_name="first name",null=True,blank=True)
    last_name = models.CharField(max_length=200,verbose_name="last name",null=True,blank=True)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")],null=True)
    age = models.CharField("age",max_length=100,null=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    profile_pic= models.ImageField(upload_to='PatientProfilePic/',default='PatientProfilePic/default.jpg',verbose_name="profile picture",null=True,blank=True)
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    class Meta:
        verbose_name_plural = "Outpatients Profiles"

class Inpatient(Entity):
    full_name = models.CharField("Full Name",max_length=255,null=True)
    age = models.CharField("Age",max_length=100)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")])
    address = models.CharField("Address",max_length=255,null=True)
    problem = models.CharField("Problem",max_length=255,null=True)
    phone =  models.CharField("Phone Number",max_length=13,null=True)
    date_admitted=models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta:
        verbose_name = "Inpatient"
        verbose_name_plural = "Inpatients"

class Appointment(Entity):
    patient=models.ForeignKey(OutPatients,on_delete=models.SET_NULL,null=True,related_name='appoinments')
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='appointments')
    symptoms = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=500)
    sending_date=models.DateTimeField(verbose_name="Sending date",default=timezone.now)
    visit_date = models.DateTimeField(verbose_name="Visit date",null=True,blank=True)
    status = models.CharField(max_length=100,choices=[("pending","pending"),("requested","requested"),("completed","completed")])

    class Meta:
        verbose_name = "Outpatient Appoinntment"
        verbose_name_plural = "Outpatients Appoinntments"

    def __str__(self) -> str:
        return f"Patient  ({self.symptoms})"

class InpatientAppointments(Entity):
    full_name = models.CharField(verbose_name="Full Name",max_length=100,null=False)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='AppointmentFormReceptiontst')
    symptoms = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=500)
    visit_date = models.DateTimeField(verbose_name="Visit date",null=True,blank=True)
    status = models.CharField(max_length=100,choices=[("pending","pending"),("requested","requested"),("completed","completed")])
    
    class Meta:
        verbose_name = "Inpatient Appoinntment"
        verbose_name_plural = "Inpatients Appoinntments"

    def __str__(self) -> str:
        return f"Patient  ({self.full_name})"

class Prescription(Entity):
    prescribe = models.CharField(max_length=1000,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    patient = models.ForeignKey('hospital.OutPatients',on_delete=models.SET_NULL,null=True,related_name='prescription')
    doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='prescription')
    created_date = models.DateTimeField(auto_now=True,null=True,blank=True,verbose_name="created date")
    #date prescribed
    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = "Prescriptions"
        
    def __str__(self) -> str:
        return f"Prescription  ({self.prescribe})"
 

    

class Room_Allotments(Entity):
    room_number = models.IntegerField(verbose_name="Room Number")
    room_type = models.CharField(verbose_name="Room Type",max_length=100)
    patient_name = models.CharField(verbose_name="Patient Name",max_length=200)
    patient_name = models.CharField(verbose_name="Patient Name",max_length=200)
    allotment_date = models.CharField(verbose_name="Allotment Date",max_length=200)
    discharge_date = models.CharField(verbose_name=" Discharge Date",max_length=200)
    doctor_name = models.CharField(verbose_name=" Doctor Name",max_length=200)

    class Meta:
        verbose_name = 'Room Allotment'
        verbose_name_plural = "Room Allotments"


class Medicine(models.Model):
    MEDICINE_NAME = models.CharField(verbose_name="Medicine Name",max_length=500)
    SELLING_PRICE = models.IntegerField(verbose_name="Selling Price")
    EXPIRE_DATE = models.DateField(verbose_name="Expire Date")
    MANUFACTURE_NAME = models.CharField(verbose_name="Manufacture Name",max_length=500)
    UNITARY_PRICE = models.IntegerField(verbose_name="Unitary Price")
    QUANTITY = models.IntegerField(verbose_name="Quantity")

    def is_expired(self):
        d = self.EXPIRE_DATE
        date2 = datetime(d.year, d.month, d.day)
        if date2 < datetime.now() :
            return "Expired"
        else :
            return "Not Expired"
    class Meta:
        verbose_name = 'Medicine'
        verbose_name_plural = "Medicines"

    


    def __str__(self) -> str:
        return self.MEDICINE_NAME

class Surgery(Entity):
    name = models.CharField("Name",max_length=255,null=True)
    age = models.CharField("age",max_length=100)
    weight = models.CharField("Weight",max_length=100)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("fmale","fmale")])
    number = models.CharField(verbose_name="Number",max_length=100)
    Ward = models.CharField("Ward",max_length=100)
    Bed = models.CharField("Bed",max_length=100)
    diagnoses = models.CharField("Diagnoses",max_length=255)
    operation_type = models.CharField("Operation Type",max_length=255)
    entry_date_time = models.DateTimeField("entry date time",auto_now_add=True)
    operation_date_time = models.DateTimeField("operation date time",auto_now_add=False)
    leaving_date_time = models.DateTimeField("leaving date time",auto_now_add=False)
    medications = models.TextField("Medications")
    operative_finding = models.TextField("operative finding",max_length=255)
    operative_procedure = models.TextField("operative procedure",max_length=255)
    operative_note = models.TextField("operative note",max_length=255)
    specimen_to_laboratory = models.BooleanField("specimen to laboratory")
    consultant_surgeon = models.CharField("consultant surgeon",max_length=255)
    co_surgeon = models.CharField("co_surgeon",max_length=255)
    surgeon = models.CharField("surgeon",max_length=255)
    anesthetist =models.CharField("anesthetist",max_length=255)
    nurse = models.ForeignKey("staff.nurse",verbose_name="Nurse",null=True,on_delete=models.SET_NULL)
    sponge_nurse = models.CharField("sponge_nurse",max_length=255)
    doctor_name = models.ForeignKey("staff.Doctor",verbose_name="Doctor",null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Surgical record'
        verbose_name_plural = "Surgical record"

    def __str__(self) -> str:
        return self.name


class Contact(Entity):
    name = models.CharField(max_length=200,verbose_name="Name")
    phone_number = models.CharField(max_length=12,verbose_name="Phone Number")
    subject = models.TextField(verbose_name=" Message")
    created = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Faq(Entity):
    question = models.CharField(max_length=120)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Gallery(Entity):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Galleries"

class Slider(Entity):
    caption = models.CharField(max_length=150)
    slogan = models.CharField(max_length=120)
    image = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.caption[:20]
    class Meta:
        verbose_name_plural = 'Slider'

class Service(Entity):
    title = models.CharField(max_length=120)
    description = models.TextField()
    items = models.ManyToManyField(to='Item',)
    thumbnail = models.ImageField(upload_to='services/')
    cover = models.ImageField(upload_to='services/')
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class Item(Entity):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Heart_Care_Basics(Entity):
    title = models.CharField(max_length=250)
    book = models.FileField('pdf', upload_to='pdf/',null=True,blank=True)
    class Meta:
        verbose_name_plural = "Heart Care Basicses"


class Department(Entity):
    name = models.CharField(verbose_name = "Name",max_length=250)
    description = models.CharField(verbose_name="Description",max_length=500)
    is_active = models.BooleanField(verbose_name="Activae",default=True)

    def __str__(self) -> str:
        return f'{self.name}'


"""
class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]

from email.policy import default
from pyexpat import model
from tabnanny import verbose


    @property
    def ordered(self):
        return self.user.id
"""