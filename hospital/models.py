from pyexpat import model
from django.db import models
from django.contrib.auth import get_user_model

from config.utils.models import Entity
User = get_user_model()
from django.utils import timezone


class Doctor(Entity):
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


class OutPatients(Entity):
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
        verbose_name_plural = "OutPatients Profiles"

class Inpatient(Entity):
    full_name = models.CharField("Full Name",max_length=255,null=True)
    age = models.CharField("Age",max_length=100)
    gender = models.CharField("Gender",max_length=100,choices=[("male","male"),("female","female")])
    address = models.CharField("Address",max_length=255,null=True)
    problem = models.CharField("Problem",max_length=255,null=True)
    phone =  models.CharField("Phone Number",max_length=13,null=True)

class Appointment(Entity):
    patient=models.ForeignKey('hospital.OutPatients',on_delete=models.SET_NULL,null=True,related_name='appoinments')
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='appointments')
    symptoms = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=500)
    sending_date=models.DateTimeField(verbose_name="Sending date",default=timezone.now)
    visit_date = models.DateTimeField(verbose_name="Visit date",null=True,blank=True)
    status = models.CharField(max_length=100,choices=[("pending","pending"),("requested","requested"),("completed","completed")])
    def __str__(self) -> str:
        return f"Patient  ({self.symptoms})"

class AppointmentFromReceptiontst(Entity):
    full_name = models.CharField(verbose_name="Full Name",max_length=100,null=False)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,related_name='AppointmentFormReceptiontst')
    symptoms = models.CharField(max_length=100,null=False)
    description=models.TextField(max_length=500)
    visit_date = models.DateTimeField(verbose_name="Visit date",null=True,blank=True)
    status = models.CharField(max_length=100,choices=[("pending","pending"),("requested","requested"),("completed","completed")])
    def __str__(self) -> str:
        return f"Patient  ({self.full_name})"

class Prescription(Entity):
    prescription = models.CharField(max_length=1000,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    patient = models.ForeignKey('hospital.OutPatients',on_delete=models.SET_NULL,null=True,related_name='prescription')
    doctor = models.ForeignKey('hospital.doctor',on_delete=models.SET_NULL,null=True,related_name='prescription')
    created_date = models.DateTimeField(verbose_name="created date",default=timezone.now)
    
    class Meta:
        verbose_name = 'Prescription'
        verbose_name_plural = "Prescriptions"
        
    def __str__(self) -> str:
        return f"Prescription  ({self.prescription})"


    

class Room_Allotments(Entity):
    pass 



class Expertize(Entity):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


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