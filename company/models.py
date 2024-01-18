from django.db import models
from users.models import User
# Create your models here.
class Company(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True, blank=True)
    industry = models.CharField(max_length=100 , null=True, blank=True)
    website = models.CharField(max_length=100 , null=True, blank=True)
    about = models.CharField(max_length=1000 , null=True, blank=True)
    
    LOCATION = (
       ('Tehran'),
       ('Esfahan'),
       ('Shiraz'),
       ('Mashhad'),
       ('Tabriz')
    )
    location = models.CharField(
        max_length=32,
        choices=LOCATION,
        default='Tehran'
    )

    SIZE = (
       ('-10'),
       ('10-50'),
       ('50-200'),
       ('200-500'),
       ('500+')
    )
    size = models.CharField(
        max_length=32,
        choices=SIZE,
        default='-10'
    )

    logo = models.ImageField(upload_to ='uploads/logo/', null=True, blank=True)

    def __str__(self):
        return self.name