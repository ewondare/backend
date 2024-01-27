import json
from django.test import TestCase, Client
from django.urls import reverse
from .models import Company
from users.models import User

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient , APITestCase
from rest_framework import status
from job.models import Job , Industry , ApplyJob
from company.models import Company


from users.models import User
from resume.models import Resume
from rest_framework.authtoken.models import Token

class UpdateCompanyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('update-company-api')

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user3 = User.objects.create(username = 'gmail3@main.com' , email='gmail3@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user4 = User.objects.create(username = 'gmail4@main.com' , email='gmail4@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)


        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')

        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry2 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        

        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title1', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')

        self.job2 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Senior',user = self.user2 , company = self.company1 ,  title='title2', is_available=True,
        description='good job',salary = 300000 , industry =self.industry2 ,qualifications ='skill2' , responsibilities ='res2')

        
        
        self.resume1 = Resume.objects.create(
            user=self.user1,
            name='John',
            lastName='Doe',
            age=20,
            gender='Male',
            about='Lorem ipsum dolor sit amet.',
            phone_number='1234567890',
            birthday='1996-01-01',
            location='Tehran',
            skills='Python, Django',
            experiences='2 years of experience',
            certifications='Certified in XYZ',
            education='Bachelor of Science',
        )

        self.resume2 = Resume.objects.create(
            user=self.user3,
            name='name3',
            lastName='lastname3',
            age=20,
            gender='Female',
            about='very shy',
            phone_number='0987654321',
            birthday='2002-12-01',
            location='Shiraz',
            skills='Python, Django, C++',
            experiences='5 years of experience',
            certifications='Certified in YTR',
            education='Cs student',
        )
        self.valid_payload = {
            'name': 'company A',
            'location' : 'Mashhad',
            'size' : '10-50',
        }
        self.invalid_payload = {
            'location' : 'Aligodarz',
            'size' : '10-30',
        }
    
    def test_update_company_api_with_valid_data(self):
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your company data has been updated!', response.data['message'])
        
        
    def test_update_company_api_with_invalid_data(self):
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Something went wrong:', response.data['message'])
        
    
    def test_update_company_api_without_recruiter_permission(self):
        self.client.force_login(self.user3)
        self.client.force_authenticate(user=self.user3)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Permission Denied.', response.data['message'])
        
    
    def test_update_company_api_unauthenticated(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 403) 
        
        

class CompanyDetailsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        
        self.industry1 = Industry.objects.create(name = 'programming')
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        

        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='Software Engineer', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')

        self.job2 = Job.objects.create(job_type ='Remote',job_experience_needed ='Senior',user = self.user2 , company = self.company1 ,  title='Electical Engineer', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill2' , responsibilities ='res2')

        
        
        self.resume1 = Resume.objects.create(
            user=self.user1,
            name='John',
            lastName='Doe',
            age=20,
            gender='Male',
            about='Lorem ipsum dolor sit amet.',
            phone_number='1234567890',
            birthday='1996-01-01',
            location='Tehran',
            skills='Python, Django',
            experiences='2 years of experience',
            certifications='Certified in XYZ',
            education='Bachelor of Science',
        )
        self.url = reverse('company-details-api')
    
    def test_company_details_api_with_valid_user(self):
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['company']['name'], self.company1.name)

        self.assertEqual(len(response.data['jobs']), 2)
        

    def test_company_details_api_with_invalid_user(self):
        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)
        self.assertIn('Company not found.', response.data['message'])
        