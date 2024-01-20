from django.urls import path
from . import views, api_views

urlpatterns = [
    path('update-resume/' , views.update_resume, name='update-resume'),
    path('resume-details/', views.resume_details, name='resume-details'),

    path('api/update-resume/', api_views.update_resume_api, name='update-resume-api'),
    path('api/recommended-jobs/', api_views.recommended_jobs_api, name='recommended-jobs-api'),
]

