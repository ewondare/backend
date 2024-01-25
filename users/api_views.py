from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login , logout
from .models import User
from .form import RegisterUserForm
from resume.models import Resume
from company.models import Company
from django.middleware.csrf import get_token
from django.db import IntegrityError

@api_view(['POST'])
def register_applicant_api(request):
    """
    Register a new applicant user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing the following fields:
            - message (str): A message indicating the result of the registration.
            - userid (int): The ID of the registered user.
            - token (str): The CSRF token for the registered user.

    Raises:
        IntegrityError: If a user with the same email or username already exists.

    Example JSON response:
        {
            "message": "Your account has been created successfully.",
            "userid": 1,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxx"
        }
    """

    form = RegisterUserForm(request.data)
    if form.is_valid():
        try:
            user = form.save(commit=False)
            user.username = user.email
            user.is_applicant = True
            user.save()
            Resume.objects.create(user=user)
            userid = user.id
            token = get_token(request)
            response_data = {
                'message': 'Your account has been created successfully.',
                'userid': userid,
                'token': token
            }
            return Response(response_data, status=201)
        except IntegrityError:
            error_message = 'A user with the same email or username already exists.'
            response_data = {'message': error_message}
            return Response(response_data, status=400)

    else:
        error_message = form.errors.as_text()
        response_data = {'message': error_message}
        return Response(response_data, status=400)
    
@api_view(['POST'])
def register_recruiter_api(request):
    """
    Register a new recruiter user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing the following fields:
            - message (str): A message indicating the result of the registration.
            - userid (int): The ID of the registered user.
            - token (str): The CSRF token for the registered user.

    Raises:
        IntegrityError: If a user with the same email or username already exists.

    Example JSON response:
        {
            "message": "Your account has been created successfully.",
            "userid": 1,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxx"
        }
    """

    form = RegisterUserForm(request.data)
    if form.is_valid():
        try:
            user = form.save(commit=False)
            user.username = user.email
            user.is_applicant = True
            user.save()
            Company.objects.create(user=user)
            userid = user.id
            token = get_token(request)
            response_data = {
                'message': 'Your account has been created successfully.',
                'userid': userid,
                'token': token
            }
            return Response(response_data, status=201)
        except IntegrityError:
            error_message = 'A user with the same email or username already exists.'
            response_data = {'message': error_message}
            return Response(response_data, status=400)
    else:
        error_message = form.errors.as_text()
        response_data = {'message': error_message}
        return Response(response_data, status=400)

@api_view(['POST'])
def login_user_api(request):
    """
    Log in a user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A JSON response containing the following fields:
            - message (str): A message indicating the result of the login.
            - token (str): The CSRF token for the logged-in user.

    Example JSON response:
        {
            "message": "Successfully logged in.",
            "token": "xxxxxxxxxxxxxxxxxxxxxxxx"
        }
    """

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