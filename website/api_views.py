from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from job.models import Job


@api_view(['GET'])
def last_jobs_api(request):
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def search_job_api(request):
    title = request.GET.get('title')
    location = request.GET.get('location')
    
    jobs = Job.objects.filter(is_available=True)

    if title:
        jobs = jobs.filter(title__icontains=title)
    
    if location:
        jobs = jobs.filter(company__location__icontains=location)
    
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)