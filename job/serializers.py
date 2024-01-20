from rest_framework import serializers
from .models import Job, ApplyJob
from resume.models import Resume

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class ApplyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'
 