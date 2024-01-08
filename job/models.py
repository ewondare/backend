from django.db import models
from users.models import User
from company.models import Company
# Create your models here.
class Job(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        company = models.ForeignKey(Company, on_delete=models.CASCADE)
        title = models.CharField(max_length=100)
        location = models.CharField(max_length=1000)
        salary = models.PositiveBigIntegerField()
        description = models.TextField()
        is_available = models.BooleanField(default=True)
        timestamp = models.DateTimeField(auto_now_add = True)

def __str__(self):
        return self.title
        

