from rest_framework import serializers
from .models import Resume
from ..job.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'