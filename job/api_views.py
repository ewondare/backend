from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobSerializer, ApplyJobSerializer, ResumeSerializer
from .form import CreateJobForm, UpdateJobForm
from job.models import Job, ApplyJob
from resume.models import Resume

@api_view(['GET'])
def job_details_api(request, pk):
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
def company_jobs_api(request, company_id):
    if request.user.is_recruiter and request.user.company_id == company_id:
        try:
            company_jobs = Job.objects.filter(company_id=company_id)
            jobs_serializer = JobSerializer(company_jobs, many=True)
            return Response(jobs_serializer.data, status=200)
        
        except Exception as e:
            response_data = {'message': str(e)}
            return Response(response_data, status=500)
    
    response_data = {'message': 'Permission denied.'}
    return Response(response_data, status=403)
    
@api_view(['GET'])
def job_resumes_api(request, pk):
    try:
        job = Job.objects.get(pk=pk)

        job_serializer = JobSerializer(job)
        resumes = Resume.objects.filter(job=job)
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
    try:
        resume = Resume.objects.get(user_id=user_id)
        apply_job = ApplyJob.objects.get(job_id=job_id, resume=resume)
        
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
    if request.user.is_recruiter and request.user.has_company:
        try:
            job = Job.objects.get(pk=pk)
            
            form = UpdateJobForm(request.POST, instance=job)
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