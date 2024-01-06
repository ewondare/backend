from django.db import models
from users.models import User

# Create your models here.

class Resume(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=100 , null=True , blank=True)
    lastName = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField( null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    about = models.CharField(max_length=1000 , null=True, blank=True)
    phone_number = models.CharField(max_length=11,null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    # insert cv 
    def __str__(self):
        return f'{self.name} {self.lastName}'