from django.urls import path
from . import api_views

urlpatterns = [
    path('api/update-company/', api_views.update_company_api, name='update-company-api'),
    path('api/company-details/', api_views.company_details_api , name='company-details-api'),
]