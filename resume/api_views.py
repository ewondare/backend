from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Resume
from .form import UpdateResumeForm
from django.contrib.auth.models import User
from job.models import Job
from .serializers import JobSerializer

@api_view(['POST'])
def update_resume_api(request):
    if request.user.is_authenticated and request.user.is_applicant:
        try:
            resume = Resume.objects.get(user=request.user)
            
            form = UpdateResumeForm(request.data, request.FILES, instance=resume)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                user.has_resume = True
                user.save()
                var.save()
                response_data = {'message': 'Your Resume has been updated.'}
                return Response(response_data, status=200)
            else:
                error_message = form.errors.as_text()
                response_data = {'message': f'Something went wrong: {error_message}'}
                return Response(response_data, status=400)
        
        except Resume.DoesNotExist:
            response_data = {'message': 'Resume not found.'}
            return Response(response_data, status=404)
    
    else:
        response_data = {'message': 'Permission denied.'}
        return Response(response_data, status=403)
    

def get_recommended_jobs(user, number_of_jobs):
    resume = user.resume
    
    user_location = resume.location
    
    recommended_jobs = Job.objects.filter(company__location=user_location, is_available=True)[:number_of_jobs]
    
    return recommended_jobs

@api_view(['GET'])
def recommended_jobs_api(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Get recommended jobs based on the user's location
        number_of_jobs = 5
        recommended_jobs = get_recommended_jobs(user, number_of_jobs)
        
        jobs_serializer = JobSerializer(recommended_jobs, many=True)
        
        response_data = {
            'recommended_jobs': jobs_serializer.data
        }
        
        return Response(response_data, status=200)
    
    except User.DoesNotExist:
        response_data = {'message': 'User not found.'}
        return Response(response_data, status=404)
    
    except Exception as e:
        response_data = {'message': str(e)}
        return Response(response_data, status=500)