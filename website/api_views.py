from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from job.models import Job


@api_view(['GET'])
def last_jobs_api(request):
    try:
        jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_message = 'An error occurred while retrieving the last jobs.'
        response_data = {'message': error_message, 'error': str(e)}
        return Response(response_data, status=400)

@api_view(['GET'])
def search_job_api(request):
    try:
        title = request.GET.get('title')
        location = request.GET.get('location')

        jobs = Job.objects.filter(is_available=True)

        if title:
            jobs = jobs.filter(title__icontains=title)

        if location:
            jobs = jobs.filter(company__location__icontains=location)

        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)
    except Exception as e:
        error_message = 'An error occurred while searching for jobs.'
        response_data = {'message': error_message, 'error': str(e)}
        return Response(response_data, status=400)