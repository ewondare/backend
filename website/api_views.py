from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from job.models import Job

@api_view(['GET'])
def job_listing_api(request):
    jobs = Job.objects.filter(is_available=True)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def job_details_api(request, pk):
    try:
        job = Job.objects.get(pk=pk)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response({'message': 'Job not found'}, status=404)