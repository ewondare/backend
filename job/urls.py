from django.urls import path
from . import views, api_views

urlpatterns = [
    path('create-job/', views.create_job, name='create-job'),
    path('update-job/<int:pk>', views.update_job, name='update-job'),
    path('manage-jobs/', views.manage_jobs, name='manage-jobs'),
    path('apply-to-job/<int:pk>/' , views.apply_to_job , name='apply-to-job'),
    path('all-applicants/<int:pk>' , views.all_applicants , name='all-applicants'),
    path('applied-jobs' , views.applied_jobs , name='applied-jobs'),

    path('api/job-details/<int:pk>', api_views.job_details_api, name='job-details-api'),
    path('api/create-job', api_views.create_job_api, name='create-job-api'),
    path('api/company-jobs', api_views.company_jobs_api, name='company-jobs-api'),
    path('api/job-resumes/<int:pk>', api_views.job_resumes_api, name='job-resumes-api'),
    path('api/specific-resume/<int:job_id>/<int:user_id>/', api_views.specific_resume_api, name='specific-resume-api'),
    path('api/update-applyjob-status/<int:job_id>/<int:user_id>/', api_views.update_applyjob_status_api, name='update-applyjob-status-api'),
    path('api/applied-jobs/', api_views.applied_jobs_api, name='applied-jobs-api'),
    path('api/update-job/<int:pk>', api_views.update_job_api, name='update-job-api'),
    path('api/apply-to-job/<int:pk>', api_views.apply_to_job_api, name='apply-to-job-api'),
]