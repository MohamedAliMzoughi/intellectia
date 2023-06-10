from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    GENDERS = [
        ('1', 'Male'),
        ('2', 'Female'),
    ]

    PAYMENTS = [
        ('1', 'Monthly'),
        ('2', 'Yearly'),
        ('3', 'Freemuim'),
    ]

    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phoneNumber = models.BigIntegerField()
    adress = models.CharField(max_length=50)
    username = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=30)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices = GENDERS)
    type = models.CharField(max_length=20)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    attemps = models.IntegerField(default=3)
    payement_method = models.CharField(max_length=10, choices = PAYMENTS,default=3)
    payed = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

class Teacher(User):
    matricule = models.BigIntegerField()
    email = models.CharField(max_length=50)
    

class Classes(models.Model):
    GRADES = [
        ('1','1st grade'),
        ('2','2nd grade'),
        ('3','3rd grade'),
        ('4','4th grade'),
        ('5','5th grade'),
        ('6','6th grade'),
    ]

    id = models.AutoField(primary_key=True)
    level = models.CharField(max_length=10, choices = GRADES)
    designiation = models.CharField(max_length=20, null=False)
    teachers = models.ManyToManyField(Teacher)  

    USERNAME_FIELD = 'designiation'

class Parent(User): 
    matricule = models.BigIntegerField()
    email = models.CharField(max_length=50)

class Student(User):
    matricule = models.BigIntegerField()
    father = models.ManyToManyField(Parent)
    grade = models.ManyToManyField(Classes)

class History(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=300)
    student = models.ManyToManyField(Student)

class Quiz(models.Model):
    id = models.AutoField(primary_key=True)
    questions = models.JSONField()
    types = models.JSONField()
    answer = models.JSONField()
    correctAnswers = models.JSONField()
    note = models.IntegerField(default=0)
    quizDate = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)


