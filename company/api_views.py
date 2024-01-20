from rest_framework.decorators import api_view
from rest_framework.response import Response
from .form import UpdateCompanyForm
from .models import Company
from users.models import User
from django.middleware.csrf import get_token
from .serializers import JobSerializer
from job.models import Job
from .serializers import CompanySerializer, JobSerializer

@api_view(['POST'])
def update_company_api(request):
    if request.user.is_recruiter:
        company = Company.objects.get(user=request.user)
        form = UpdateCompanyForm(request.data, instance=company)
        if form.is_valid():
            var = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            user.has_company = True
            var.save()
            user.save()
            
            token = get_token(request)
            response_data = {
                'message': 'Your company data has been updated!',
                'token': token
            }
            return Response(response_data, status=200)
        else:
            error_message = form.errors.as_text()
            response_data = {'message': f'Something went wrong: {error_message}'}
            return Response(response_data, status=400)
    else:
        response_data = {'message': 'Permission Denied.'}
        return Response(response_data, status=403)

@api_view(['GET'])
def company_details_api(request, pk):
    try:
        company = Company.objects.get(pk=pk)
        jobs = Job.objects.filter(company=company)
        company_serializer = CompanySerializer(company)
        jobs_serializer = JobSerializer(jobs, many=True)
        response_data = {
            'company': company_serializer.data,
            'jobs': jobs_serializer.data
        }
        return Response(response_data, status=200)
    except Company.DoesNotExist:
        response_data = {'message': 'Company not found.'}
        return Response(response_data, status=404)