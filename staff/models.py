from operator import imod
from tabnanny import verbose
from django.db import models

from config.utils.models import Entity
from hospital.models import User


class Nurse(Entity):
    name = models.CharField(verbose_name="Name ",max_length=100)
    salary = models.IntegerField(verbose_name="Salary ")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField("Gender",max_length=100,choices=(("male","male"),("female","female")))
    derpartment = models.CharField(verbose_name="Derpartment",max_length=100)
    work_time = models.CharField(verbose_name="work time",max_length=500)
    workdays = models.CharField(verbose_name="workdays",max_length=500)
    picture = models.ImageField(upload_to="nures/")
    class Meta :
        verbose_name = "Nures "
        verbose_name_plural = "Nurses"

class OtherEmployee(Entity):
    name = models.CharField(verbose_name="Name ",max_length=100)
    salary = models.IntegerField(verbose_name="Salary ")
    age = models.IntegerField(verbose_name="Age")
    gender = models.CharField("Gender",max_length=100,choices=(("male","male"),("female","female")))
    type_of_job = models.CharField(verbose_name="Type Of Job ",max_length=300)
    derpartment = models.CharField(verbose_name="Derpartment",max_length=100)
    work_time = models.CharField(verbose_name="work time",max_length=500)
    workdays = models.CharField(verbose_name="workdays",max_length=500)
    picture = models.ImageField(upload_to="employee/")

    class Meta :
        verbose_name = "Other Employee"
        verbose_name_plural = "Other Employees"


class Expertize(Entity):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Doctor(Entity):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="first name",max_length=120)
    last_name = models.CharField(verbose_name="last name",max_length=120)
    gender = models.CharField("Gender",max_length=100,choices=(("male","male"),("female","female")))
    age = models.CharField("age",max_length=100,null=True) 
    speciality = models.CharField(max_length=120)
    picture = models.ImageField(upload_to="doctors/")
    address = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=20,null=True)
    experience = models.CharField(max_length=250,verbose_name="Experience in year")
    expertize = models.ManyToManyField(to='Expertize', related_name='doctors',null=True,blank=True)
    availability = models.CharField(verbose_name="Availability",max_length=20,choices=(("Available","Available"),("On Leave","On Leave"),("Not Available","Not Available")))
    working_days = models.CharField(max_length=250,verbose_name="workdays") 

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
