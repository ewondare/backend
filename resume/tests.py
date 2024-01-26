import json
from django.test import TestCase, Client 
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Resume
from users.models import User
from job.models import Job , Industry , ApplyJob
from company.models import Company
from .api_views import get_recommended_jobs
from rest_framework import status




class UpdateResumeAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('update-resume-api')
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
    
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
            'gender' : 'Female',
            'phone_number' : '0987654321',
            'location' : 'Tabriz'
        }

        self.invalid_payload = {
            'gender' : 'Transgender',
            'phone_number' : '0987654321',
            'location' : 'Shiraz'
        }
    
    def test_update_resume_api_with_valid_data(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Your Resume has been updated.', response.data['message'])

      
    def test_update_resume_api_with_invalid_data(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Something went wrong:', response.data['message'])
      
    def test_update_resume_api_without_applicant_permission(self):
        
        self.client.force_login(self.user2)
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 403)
        self.assertIn('Permission denied.', response.data['message'])

       
    def test_update_resume_api_unauthenticated(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, 403)
        
class GetRecommendedJobsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('update-resume-api')
       
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
       
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title1', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')

        self.job2 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Senior',user = self.user2 , company = self.company1 ,  title='title2', is_available=True,
        description='good job',salary = 300000 , industry =self.industry1 ,qualifications ='skill2' , responsibilities ='res2')
        
        self.job3 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Intern',user = self.user2 , company = self.company1 ,  title='title3', is_available=False,
        description='good job',salary = 163849 , industry =self.industry1 ,qualifications ='skill3' , responsibilities ='res3')
        
        self.job4 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title4', is_available=False,
        description='good job',salary = 63728 , industry =self.industry1 ,qualifications ='skill4' , responsibilities ='res4')
        
        
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

    def test_get_recommended_jobs(self):
        recommended_jobs = get_recommended_jobs(self.user1, number_of_jobs=2)
        self.assertEqual(len(recommended_jobs), 2)
        self.assertIn(self.job1, recommended_jobs)
        self.assertIn(self.job2, recommended_jobs)
        self.assertNotIn(self.job3, recommended_jobs)
        self.assertNotIn(self.job4, recommended_jobs)



class RecommendedJobsAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        
       
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user4 = User.objects.create(username = 'gmail4@main.com' , email='gmail4@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry1 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        
        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title1', is_available=True,
        description='good job',salary = 200000 , industry =self.industry1 ,qualifications ='skill1' , responsibilities ='res1')

        self.job2 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Senior',user = self.user2 , company = self.company1 ,  title='title2', is_available=True,
        description='good job',salary = 300000 , industry =self.industry1 ,qualifications ='skill2' , responsibilities ='res2')
        
        self.job3 = Job.objects.create(job_type ='Onsite',job_experience_needed ='Intern',user = self.user2 , company = self.company2,  title='title3', is_available=True,
        description='good job',salary = 163849 , industry =self.industry1 ,qualifications ='skill3' , responsibilities ='res3')
        
        self.job4 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='title4', is_available=False,
        description='good job',salary = 63728 , industry =self.industry1 ,qualifications ='skill4' , responsibilities ='res4')
        
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

    def test_recommended_jobs_api(self):
        url = reverse('recommended-jobs-api', args=[self.user1.id])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = response.json()
        recommended_jobs = response_data['recommended_jobs']
        
        self.assertEqual(len(recommended_jobs), 2)
        self.assertEqual(recommended_jobs[0]['title'], 'title1')
        self.assertEqual(recommended_jobs[1]['title'], 'title2')
    
    def test_recommended_jobs_api_invalid_user(self):
        url = reverse('recommended-jobs-api', args=[999])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        response_data = response.json()
        self.assertEqual(response_data['message'], 'User not found.')
    
