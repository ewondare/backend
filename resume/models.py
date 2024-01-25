from django.db import models
from users.models import User

class Resume(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True)
    lastName = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True, blank=True)

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        )
    gender = models.CharField(
            max_length=10,
            choices=GENDER_CHOICES,
            default='Male'
    )

    about = models.CharField(max_length=1000 , null=True, blank=True)
    phone_number = models.CharField(max_length=11,null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)

    LOCATION_CHOICES = (
        ('Tehran', 'Tehran'),
        ('Esfahan', 'Esfahan'),
        ('Shiraz', 'Shiraz'),
        ('Mashhad', 'Mashhad'),
        ('Tabriz', 'Tabriz')
    )
    location = models.CharField(
        max_length=32,
        choices=LOCATION_CHOICES,
        default='Tehran'
    )

    skills = models.CharField(max_length=500 , null=True, blank=True)
    experiences = models.CharField(max_length=1000 , null=True, blank=True)
    certifications = models.CharField(max_length=1000 , null=True, blank=True)
    education = models.CharField(max_length=1000 , null=True, blank=True)
    photo = models.ImageField(upload_to ='uploads/photo/', null=True, blank=True)
    upload_resume = models.FileField(upload_to='uploads/resume_file/', blank=True)

    def __str__(self):
        return f'{self.name} {self.lastName}'