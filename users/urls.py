from django.urls import path
from . import api_views

urlpatterns = [
    path('api/register-applicant/', api_views.register_applicant_api, name='register-applicant-api'),
    path('api/register-recruiter/', api_views.register_recruiter_api, name='register-recruiter-api'),
    path('api/login-user/', api_views.login_user_api, name='login-user-api'),
    path('api/logout-user/', api_views.logout_user_api, name='logout-user-api'),
]