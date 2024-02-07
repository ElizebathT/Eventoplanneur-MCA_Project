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
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()  
    def __str__(self):
        return self.email
    
   
class EventOrganizer(models.Model):
    name = models.CharField(max_length=255)
    emails = models.EmailField(unique=True,blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    college = models.BooleanField(default=True) 
    aicte = models.CharField(max_length=255, blank=True, null=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    location = models.CharField(max_length=100,null=True)
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
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='offline')
    description = models.TextField()
    date = models.DateField(default=None, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    poster = models.URLField(blank=True, null=True) 
    organizer_name = models.CharField(max_length=100)  
    deadline = models.DateField(default=None, blank=True, null=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  
    speakers = models.ManyToManyField(Speaker, blank=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    livestream = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    max_participants = models.PositiveIntegerField(null=True,default=50) 
    status = models.IntegerField(default=1,null=True,blank=True)
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

class Conference(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    location = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField()
    organizer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    poster = models.URLField()
    livestream = models.CharField(max_length=100,blank=True, null=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    event_type = models.CharField(
        max_length=20, choices=[('Offline', 'Offline'), ('Online', 'Online')]
    )
    speakers = models.ManyToManyField(Speaker, blank=True)
    deadline = models.DateField(default=None, blank=True, null=True)
    def __str__(self):
        return self.title


class WebinarRegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE)

class Attendee(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    interests = models.TextField(blank=True, null=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
    
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='service_images/')
    locations = models.TextField(null=True)
    services_provided = models.TextField()
    description = models.TextField()
    rating = models.IntegerField(default=0,null=True)
    capacity = models.IntegerField(null=True)
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    booked_dates = models.ManyToManyField('BookedDate', blank=True)
    def add_booked_date(self, new_date):
        # Add the new date to the booked_dates relationship
        booked_date_obj, created = BookedDate.objects.get_or_create(date=new_date)
        self.booked_dates.add(booked_date_obj)
        self.save()

        # Return the updated booked dates as a string
        return ', '.join(str(date) for date in self.booked_dates.all())

    def __str__(self):
        return self.name
    
class BookService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    services_required = models.TextField()
    budget = models.IntegerField()
    participants = models.IntegerField()
    date = models.DateField(null=True) 
    org_user=models.ForeignKey(CustomUser, on_delete=models.CASCADE,null=True,blank=True)
    status = models.TextField(default="pending")
    def __str__(self):
        return f"{self.service.name} - {self.location}"
    def is_current_user(self, current_user):
        return self.org_user == current_user

class BookedDate(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)