from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('job-listing', views.job_listing, name='job-listing'),
    path('job-details/<int:pk>/', views.job_details, name='job-details'),


    path('api/last-jobs/', api_views.last_jobs_api, name='last-jobs-api'),
    path('api/search-job/', api_views.search_job_api, name='search-job-api'),
]