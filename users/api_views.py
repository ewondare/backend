from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login , logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company
from django.middleware.csrf import get_token

@api_view(['POST'])
def register_applicant_api(request):
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        var = form.save(commit=False)
        var.is_applicant = True
        var.save()
        Resume.objects.create(user=var)
        userid = var.id
        token = get_token(request)
        response_data = {
            'message': 'Your account has been created successfully.',
            'userid': userid,
            'token': token
        }
        return Response(response_data, status=201)
    else:
        error_message = form.errors.as_text()
        response_data = {'message': f'Something went wrong: {error_message}'}
        return Response(response_data, status=400)
    
@api_view(['POST'])
def register_recruiter_api(request):
    form = RegisterUserForm(request.POST)
    if form.is_valid():
        var = form.save(commit=False)
        var.is_recruiter = True
        var.save()
        Company.objects.create(user=var)
        userid = var.id
        token = get_token(request)
        response_data = {
            'message': 'Your account has been created successfully.',
            'userid': userid,
            'token': token
        }
        return Response(response_data, status=201)
    else:
        error_message = form.errors.as_text()
        response_data = {'message': f'Something went wrong: {error_message}'}
        return Response(response_data, status=400)

@api_view(['POST'])
def login_user_api(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None and user.is_active:
        login(request, user)
        token = get_token(request)
        response_data = {
            'message': 'Successfully logged in.',
            'token': token
        }
        return Response(response_data, status=200)
    else:
        response_data = {'message': 'Invalid credentials. Please try again.'}
        return Response(response_data, status=400)