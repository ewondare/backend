from django.urls import path
from . import views, api_views

urlpatterns = [
    path('', views.home, name='home'),
    path('job-listing', views.job_listing, name='job-listing'),
    path('job-details/<int:pk>/', views.job_details, name='job-details'),


    path('api/job-listing/', api_views.job_listing_api, name='job-listing-api'),
    path('api/job-details/<int:pk>/', api_views.job_details_api, name='job-details-api'),
]