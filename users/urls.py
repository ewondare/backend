from django.urls import path
from . import views, api_views

urlpatterns = [
    path('register-applicant/' , views.register_applicant, name='register-applicant'),
    path('register-recruiter/' , views.register_recruiter , name='register-recruiter'),
    path('login/' , views.login_user , name='login'),
    path('logout/' , views.logout_user , name='logout'),

    path('api/register-applicant/', api_views.register_applicant_api, name='register-applicant-api'),
    path('api/register-recruiter/', api_views.register_recruiter_api, name='register-recruiter-api'),
    path('api/login-user/', api_views.login_user_api, name='login-user-api'),
]