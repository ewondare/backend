from django.db import models
from users.models import User
# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True)
    industry = models.CharField(max_length=100 , null=True, blank=True)
    website = models.CharField(max_length=100 , null=True, blank=True)
    about = models.CharField(max_length=1000 , null=True, blank=True)
    
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

    SIZE_CHOICES = (
        ('-10', 'Less than 10'),
        ('10-50', '10-50 employees'),
        ('50-200', '50-200 employees'),
        ('200-500', '200-500 employees'),
        ('500+', 'More than 500')
    )
    size = models.CharField(
        max_length=32,
        choices=SIZE_CHOICES,
        default='-10'
    )

    logo = models.ImageField(upload_to ='uploads/logo/', null=True, blank=True)

    def __str__(self):
        return self.name