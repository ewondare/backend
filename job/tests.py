from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Job
from job.models import Job , Industry , ApplyJob
from company.models import Company
from users.models import User
from resume.models import Resume

class JobDetailsAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title1', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')
        
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
         
    
    
    def test_job_details_api(self):
        url = reverse('job-details-api', kwargs={'pk': self.job1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job']['title'], 'title1')
    
    def test_job_details_api_not_found(self):
        url = reverse('job-details-api', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Job not found.')

class CreateJobAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('create-job-api')
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title10', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')
        
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
        
        self.valid_payload = {
            'title': 'title10',
            'salary': '200000',
            
        }
    
    def test_create_job_api_with_valid_data(self):
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)

        response = self.client.post(self.url, data=self.valid_payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertIn('title', response.data)
        self.assertEqual(response.data['title'], 'title10')
        
        jobs = Job.objects.filter(title='title10')
        job = jobs.first()
        self.assertEqual(job.user.id, self.user2.id)
        self.assertEqual(job.company, self.company1)

    
    def test_create_job_api_without_permissions(self):

        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)

        response = self.client.post(self.url, data=self.valid_payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        self.assertEqual(response.data['message'], 'Permission denied.')
    
    def test_create_job_api_with_invalid_data(self):

        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)

        response = self.client.post(self.url, data={})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('title', response.data)
        self.assertIn('This field is required.', response.data['title'])

class CompanyJobsAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('company-jobs-api')
         
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')
        
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title1', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')

        self.job2 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Senior',user = self.user2 , company = self.company1 ,  title='title2', is_available=True,
        description='good job',salary = 300000 , industry =self.industry2 ,qualifications ='skill2' , responsibilities ='res2')
    '''
    def test_company_jobs_api_with_valid_permissions(self):
        
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        self.assertIn('data', response.data)
        self.assertEqual(len(response.data['data']), 2)
        
        
        job_data1 = response.data['data'][0]
        self.assertEqual(job_data1['id'], self.job1.id)
        self.assertEqual(job_data1['data']['title'], self.job1.title)
        self.assertEqual(job_data1['data']['description'], self.job1.description)
        
        
        job_data2 = response.data['data'][1]
        self.assertEqual(job_data2['id'], self.job2.id)
        self.assertEqual(job_data2['data']['title'], self.job2.title)
        self.assertEqual(job_data2['data']['description'], self.job2.description)

    
    def test_company_jobs_api_without_permissions(self):

        #self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.url)

        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
        self.assertEqual(response.data['message'], 'Permission denied.')


    def setUp(self):
        self.client = Client()
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
        )'''