from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    USERNAME_FIELD  = 'email'
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_organizer = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()  
    def __str__(self):
        return self.email
    
class EventOrganizer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    college = models.BooleanField(default=True) 
    aicte = models.CharField(max_length=255, blank=True, null=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Speaker(models.Model):
    DESIGNATION_CHOICES = (
        ('Dr', 'Dr'),
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Mrs', 'Mrs'),
    )
    speaker_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=3, choices=DESIGNATION_CHOICES)
    def __str__(self):
        return f"{self.get_designation_display()} {self.speaker_name}"
    
class Webinar(models.Model):
    EVENT_TYPE_CHOICES = [
    ('Online', 'Online'),
    ('Offline', 'Offline'),
]
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='offline')
    description = models.TextField()
    date = models.DateField(default=None, blank=True, null=True)
    time = models.TimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    poster = models.URLField(blank=True, null=True) 
    organizer_name = models.CharField(max_length=100)  # Added organizer name field
    deadline = models.DateField(default=None, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Added fee field
    speakers = models.ManyToManyField(Speaker, blank=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    livestream = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    def __str__(self):
        return self.title
    
class AICTE(models.Model):
    aicte_id = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    address = models.TextField(max_length=200)
    programs_offered = models.ManyToManyField('Program', related_name='AICTE')
    departments = models.ManyToManyField('Department', related_name='AICTE')

    def __str__(self):
        return self.name

class Program(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name