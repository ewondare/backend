from django.urls import path
from . import api_views

urlpatterns = [
    path('api/last-jobs/', api_views.last_jobs_api, name='last-jobs-api'),
    path('api/search-job/', api_views.search_job_api, name='search-job-api'),
]