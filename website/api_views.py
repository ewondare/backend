from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import JobSerializer
from job.models import Job


@api_view(['GET'])
def last_jobs_api(request):
    """
    Retrieve the last available jobs.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing a list of serialized job objects.

    Raises:
        Exception: If an error occurs while retrieving the last jobs.

    Example JSON response:
        [
            {
                "id": 1,
                "title": "Job Title 1",
                "company": "Company 1",
                "location": "Location 1",
                ...
            },
            {
                "id": 2,
                "title": "Job Title 2",
                "company": "Company 2",
                "location": "Location 2",
                ...
            },
            ...
        ]

    Example JSON error response:
        {
            "message": "An error occurred while retrieving the last jobs.",
            "error": "<error_message>"
        }
    """
    
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
    """
    Search for jobs based on title and/or location.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing a list of serialized job objects.

    Raises:
        Exception: If an error occurs while searching for jobs.

    Example usage:
        GET /search_job/?title=Software&location=California

    Example JSON response:
        [
            {
                "id": 1,
                "title": "Software Developer",
                "company": "Company 1",
                "location": "California",
                ...
            },
            {
                "id": 2,
                "title": "Senior Software Engineer",
                "company": "Company 2",
                "location": "California",
                ...
            },
            ...
        ]

    Example JSON error response:
        {
            "message": "An error occurred while searching for jobs.",
            "error": "<error_message>"
        }
    """

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