from django.urls import path
from . import views, api_views

urlpatterns = [
    path('update-company/', views.update_company, name='update-company'),
    path('company-details/<int:pk>', views.company_details , name='company-details'),

    path('api/update-company/', api_views.update_company_api, name='update-company-api'),
    path('api/company-details/<int:pk>', api_views.company_details_api , name='company-details-api'),
]