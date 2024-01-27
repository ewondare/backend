from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import JobSerializer, ApplyJobSerializer, ResumeSerializer
from .form import CreateJobForm, UpdateJobForm
from job.models import Job, ApplyJob
from resume.models import Resume
from company.models import Company

@api_view(['GET'])
def job_details_api(request, pk):
    """
    Retrieve details of a specific job and related jobs.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the job to retrieve details for.

    Returns:
        Response: A JSON response containing the following fields:
            - job (dict): A serialized representation of the job.
                - id (int): The ID of the job.
                - user (int): The ID of the user who created the job.
                - company (int): The ID of the company associated with the job.
                - title (str): The title of the job.
                - salary (int): The salary of the job.
                - description (str): The description of the job.
                - is_available (bool): Indicates if the job is available or not.
                - timestamp (str): The creation timestamp of the job.
                - industry (int): The ID of the industry associated with the job.
                - job_type (str): The type of the job (e.g., 'Remote', 'Onsite', 'Hybrid').
                - job_experience_needed (str): The experience level needed for the job (e.g., 'Intern', 'Junior', 'Senior').
                - qualifications (str): The qualifications required for the job.
                - responsibilities (str): The responsibilities of the job.
            - related_jobs (list): A list of serialized representations of related jobs.

        The response has a status code of 200 (OK) if the job is found,
        or a status code of 404 (Not Found) if the job does not exist.

    Raises:
        Job.DoesNotExist: If the job with the specified primary key does not exist.
    """

    try:
        job = Job.objects.get(pk=pk)
        related_jobs = Job.objects.filter(company=job.company).exclude(pk=pk)[:3]
        
        job_serializer = JobSerializer(job)
        related_jobs_serializer = JobSerializer(related_jobs, many=True)
        
        response_data = {
            'job': job_serializer.data,
            'related_jobs': related_jobs_serializer.data
        }
        return Response(response_data, status=200)
    except Job.DoesNotExist:
        response_data = {'message': 'Job not found.'}
        return Response(response_data, status=404)
    

@api_view(['POST'])
def create_job_api(request):
    """
    Create a new job for the authenticated recruiter user.

    Args:
        request (HttpRequest): The HTTP request object containing the job data.

    Returns:
        Response: A JSON response containing the serialized representation of the created job,
        or a JSON response with form errors if the request contains invalid data.
        If the user is not a recruiter or does not have a company, the response has a status code of 403 (Forbidden).

    Raises:
        N/A
    """

    if request.user.is_recruiter and request.user.has_company:
        form = CreateJobForm(request.data)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.company = request.user.company
            job.save()
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        response_data = {'message': 'Permission denied.'}
        return Response(response_data, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
def company_jobs_api(request):
    """
    Retrieve all jobs associated with a specific company.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing a list of serialized representations of the company's jobs,
        or an error message if the user does not have permission to access the jobs.
        If the request encounters an exception, the response has a status code of 500 (Internal Server Error).

    Raises:
        N/A
    """
    try:
        company = Company.objects.get(user=request.user)
        if request.user.is_recruiter:
            try:
                company_jobs = Job.objects.filter(company_id=company.id)
                jobs_serializer = JobSerializer(company_jobs, many=True)
            
                return Response(jobs_serializer.data, status=status.HTTP_200_OK)
            
            except Exception as e:
                response_data = {'message': str(e)}
                return Response(response_data, status=500)
        
        response_data = {'message': 'Permission denied.'}
        return Response(response_data, status=403)
    except Exception as e:
        response_data = {'message': str(e)}
        return Response(response_data, status=404)
    
@api_view(['GET'])
def job_resumes_api(request, pk):
    """
    Retrieve the resumes submitted for a specific job.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the job to retrieve resumes for.

    Returns:
        Response: A JSON response containing the following fields:
            - job (dict): A serialized representation of the job.
            - resumes (list): A list of serialized representations of the resumes submitted for the job.
                - id (int): The ID of the resume.
                - user (int): The ID of the user who submitted the resume.
                - name (str): The name of the user.
                - lastName (str): The last name of the user.
                - age (int): The age of the user.
                - gender (str): The gender of the user.
                - about (str): A description about the user.
                - phone_number (str): The phone number of the user.
                - birthday (str): The birthday of the user.
                - location (str): The location of the user.
                - skills (str): The skills of the user.
                - experiences (str): The experiences of the user.
                - certifications (str): The certifications of the user.
                - education (str): The education of the user.
                - photo (str): The URL to the user's photo.
                - upload_resume (str): The URL to the uploaded resume.

        The response has a status code of 200 (OK) if the job is found,
        or a status code of 404 (Not Found) if the job does not exist.

    Raises:
        Job.DoesNotExist: If the job with the specified primary key does not exist.
   """

    try:
        job = Job.objects.get(pk=pk)

        job_serializer = JobSerializer(job)

        apply_jobs = ApplyJob.objects.filter(job=job)

        user_ids = [apply_job.user_id for apply_job in apply_jobs]

        resumes = Resume.objects.filter(user__id__in=user_ids)

        resumes_serializer = ResumeSerializer(resumes, many=True)

        response_data = {
            'job': job_serializer.data,
            'resumes': resumes_serializer.data
        }
        return Response(response_data, status=200)
    except Job.DoesNotExist:
        response_data = {'message': 'Job not found.'}
        return Response(response_data, status=404)
    
@api_view(['GET'])
def specific_resume_api(request, job_id, user_id):
    """
    Retrieve a specific resume for a job.

    Args:
        request (HttpRequest): The HTTP request object.
        job_id (int): The primary key of the job that the resume is associated with.
        user_id (int): The primary key of the user who submitted the resume.

    Returns:
        Response: A JSON response containing the following fields:
            - job (dict): A serialized representation of the job.
            - resume (dict): A serialized representation of the specific resume.

        The response has a status code of 200 (OK) if the resume is found,
        or a status code of 404 (Not Found) if the resume or job does not exist.

    Raises:
        Resume.DoesNotExist: If the resume with the specified user ID does not exist.
        ApplyJob.DoesNotExist: If the ApplyJob entry does not exist for the specified job and resume.
    """

    try:
        resume = Resume.objects.get(user_id=user_id)
        apply_job = ApplyJob.objects.get(job_id=job_id, user_id=user_id)
        
        resume_serializer = ResumeSerializer(resume)
        job_serializer = JobSerializer(apply_job.job)
        
        response_data = {
            'job': job_serializer.data,
            'resume': resume_serializer.data
        }
        return Response(response_data, status=200)
    except (Resume.DoesNotExist, ApplyJob.DoesNotExist):
        response_data = {'message': 'Resume not found for the specified job.'}
        return Response(response_data, status=404)
    
@api_view(['PUT'])
def update_applyjob_status_api(request, job_id, user_id):
    """
    Update the status of an ApplyJob entry.

    Args:
        request (HttpRequest): The HTTP request object.
        job_id (int): The primary key of the job associated with the ApplyJob entry.
        user_id (int): The primary key of the user associated with the ApplyJob entry.

    Returns:
        Response: A JSON response containing the serialized representation of the updated ApplyJob entry,
        or an error message if the ApplyJob entry is not found.

        Example:
        HTTP 200 OK
        {
            "id": 1,
            "job": 123,
            "user": 987,
            "status": "accepted"
        }

    Raises:
        ApplyJob.DoesNotExist: If the ApplyJob entry with the specified job and user IDs does not exist.
    """

    try:
        apply_job = ApplyJob.objects.get(job_id=job_id, user_id=user_id)
        status = request.data.get('status')  

        apply_job.status = status
        apply_job.save()

        serializer = ApplyJobSerializer(apply_job)
        return Response(serializer.data, status=200)
    except ApplyJob.DoesNotExist:
        response_data = {'message': 'ApplyJob not found.'}
        return Response(response_data, status=404)
    
@api_view(['GET'])
def applied_jobs_api(request):

    """
    Retrieve the jobs that a user has applied to.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing the following fields:
            - apply_jobs (list): A list of serialized representations of the user's ApplyJob entries.
            - jobs (list): A list of serialized representations of the jobs the user has applied to.

        The response has a status code of 200 (OK) if the user is authenticated and has applied to jobs,
        or a status code of 500 (Internal Server Error) if an exception occurs.

    Raises:
        N/A
    """

    try:
        user = request.user

        apply_jobs = ApplyJob.objects.filter(user=user)
        apply_jobs_serializer = ApplyJobSerializer(apply_jobs, many=True)

        jobs = [apply_job.job for apply_job in apply_jobs]
        jobs_serializer = JobSerializer(jobs, many=True)

        response_data = {
            'apply_jobs': apply_jobs_serializer.data,
            'jobs': jobs_serializer.data
        }
        return Response(response_data, status=200)
    
    except Exception as e:
        response_data = {'message': str(e)}
        return Response(response_data, status=500)
    

@api_view(['POST'])
def update_job_api(request, pk):
    """
    Update an existing job.

    Args:
        request (HttpRequest): The HTTP request object containing the updated job data.
        pk (int): The primary key of the job to update.

    Returns:
        Response: A JSON response containing a success message if the job update is successful,
        or an error message with form errors if the request contains invalid data.
        If the user is not a recruiter or does not have a company, the response has a status code of 403 (Forbidden).
        If the job with the specified primary key does not exist, the response has a status code of 404 (Not Found).
        If an exception occurs, the response has a status code of 500 (Internal Server Error).

    Raises:
        Job.DoesNotExist: If the job with the specified primary key does not exist.
    """

    if request.user.is_recruiter and request.user.has_company:
        try:
            job = Job.objects.get(pk=pk)
            
            form = UpdateJobForm(request.data, instance=job)
            if form.is_valid():
                form.save()
                response_data = {'message': 'Your Job Ad is now updated.'}
                return Response(response_data, status=200)
            
            response_data = {'message': 'Something went wrong.', 'errors': form.errors}
            return Response(response_data, status=400)
        
        except Job.DoesNotExist:
            response_data = {'message': 'Job not found.'}
            return Response(response_data, status=404)
        
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(response_data, status=500)
    
    response_data = {'message': 'Permission denied.'}
    return Response(response_data, status=403)

@api_view(['POST'])
def apply_to_job_api(request, pk):
    """
    Apply to a job as an authenticated applicant user.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the job to apply to.

    Returns:
        Response: A JSON response containing a success message if the application is successful,
        or an error message if the user is not authenticated, is not an applicant, or has already applied to the job.
        If the job with the specified primary key does not exist, the response has a status code of 404 (Not Found).
        If an exception occurs, the response has a status code of 500 (Internal Server Error).

    Raises:
        Job.DoesNotExist: If the job with the specified primary key does not exist.
    """

    if request.user.is_authenticated and request.user.is_applicant:
        try:
            job = Job.objects.get(pk=pk)
            if ApplyJob.objects.filter(user=request.user, job=job).exists():
                response_data = {'message': 'You already applied for this job.'}
                return Response(response_data, status=403)
            else:
                ApplyJob.objects.create(job=job, user=request.user, status='Pending')
                response_data = {'message': 'You have successfully applied! Please check your dashboard.'}
                return Response(response_data, status=200)
        
        except Job.DoesNotExist:
            response_data = {'message': 'Job not found.'}
            return Response(response_data, status=404)
        
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(response_data, status=500)
    
    response_data = {'message': 'Permission denied.'}
    return Response(response_data, status=401)