from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
from django.utils import timezone


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="first name",max_length=120)
    last_name = models.CharField(verbose_name="last name",max_length=120)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")],null=True)
    age = models.CharField("age",max_length=100,null=True)
    speciality = models.CharField(max_length=120)
    picture = models.ImageField(upload_to="doctors/")
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    details = models.TextField()
    experience = models.TextField()
    expertize = models.ManyToManyField(to='Expertize', related_name='doctors',null=True,blank=True)
    twitter = models.CharField(max_length=120, blank=True, null=True)
    facebook = models.CharField(max_length=120, blank=True, null=True)
    instagram = models.CharField(max_length=120, blank=True, null=True)

    @property
    def patients(self):
        return self.appointments.all().count()
    @property
    def patients_qs(self):
        return self.appointments.all()

    class Meta :
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return self.first_name


class Patient_Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,verbose_name="first name",null=True,blank=True)
    last_name = models.CharField(max_length=200,verbose_name="last name",null=True,blank=True)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")],null=True)
    age = models.CharField("age",max_length=100,null=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    profile_pic= models.ImageField(upload_to='PatientProfilePic/',verbose_name="profile picture",null=True,blank=True)
    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

    class Meta:
        verbose_name_plural = "patients profiles"


class Appointment(models.Model):
    patient=models.ForeignKey('hospital.Patient_Profile',on_delete=models.SET_NULL,null=True,related_name='appoinments')
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='appointments')
    symptoms = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=500)
    sending_date=models.DateTimeField(verbose_name="Sending date",default=timezone.now)
    visit_date = models.DateTimeField(verbose_name="Visit date",null=True,blank=True)
    status = models.CharField(max_length=100,choices=[("pending","pending"),("requested","requested"),("completed","completed")])


    def __str__(self) -> str:
        return f"Patient  ({self.symptoms})"

class Prescription(models.Model):
    prescription = models.CharField(max_length=1000,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    patient=models.ForeignKey('hospital.Patient_Profile',on_delete=models.SET_NULL,null=True,related_name='prescription')
    doctor=models.ForeignKey('hospital.doctor',on_delete=models.SET_NULL,null=True,related_name='prescription')
    created_date=models.DateTimeField(verbose_name="created date",default=timezone.now)
    def __str__(self) -> str:
        return f"Prescription  ({self.prescription})"

class Inpatient(models.Model):
    name = models.CharField("Name",max_length=255,null=True)
    age = models.CharField("age",max_length=100)
    weight = models.CharField("Weight",max_length=100)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")])
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
    nurse = models.CharField("nurse",max_length=255)
    sponge_nurse = models.CharField("sponge_nurse",max_length=255)
    doctor_name = models.CharField("doctor_name",max_length=255)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    class Meta:
        verbose_name = 'Inpatient'
        verbose_name_plural = "Inpatients"

    def __str__(self) -> str:
        return self.name



class Expertize(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=120)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Gallery(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Galleries"

class Slider(models.Model):
    caption = models.CharField(max_length=150)
    slogan = models.CharField(max_length=120)
    image = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.caption[:20]
    class Meta:
        verbose_name_plural = 'Slider'

class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    items = models.ManyToManyField(to='Item',)
    thumbnail = models.ImageField(upload_to='services/')
    cover = models.ImageField(upload_to='services/')
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=120)

    def __str__(self):
        return self.title

class Heart_Care_Basics(models.Model):
    title = models.CharField(max_length=250)
    book = models.FileField('pdf', upload_to='pdf/',null=True,blank=True)
    class Meta:
        verbose_name_plural = "Heart Care Basicses"





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