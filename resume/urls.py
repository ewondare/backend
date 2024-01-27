from django.urls import path
from . import api_views

urlpatterns = [
    path('api/update-resume/', api_views.update_resume_api, name='update-resume-api'),
    path('api/recommended-jobs/<int:user_id>', api_views.recommended_jobs_api, name='recommended-jobs-api'),
]

