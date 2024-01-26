from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient , APITestCase
from rest_framework import status
from job.models import Job , Industry , ApplyJob
from company.models import Company
from .serializers import JobSerializer
from users.models import User
from resume.models import Resume
from .api_views import last_jobs_api


class SearchJobAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search-job-api')  
        
        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        
        
        self.industry1 = Industry.objects.create(name = 'programming')
        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        
        

        self.job1 = Job.objects.create(job_type ='Remote',job_experience_needed ='Junior',user = self.user2 , company = self.company1 ,  title='Software Engineer', is_available=True,
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
        
        



    def test_search_job_without_filters(self):

        print(self.url)
        response = self.client.get(self.url)
        print(response.data)
        jobs = Job.objects.filter(is_available=True)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_job_with_title_filter(self):
        response = self.client.get(self.url, {'title': 'software'})
        jobs = Job.objects.filter(title__icontains='software', is_available=True)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_job_with_location_filter(self):
        response = self.client.get(self.url, {'location': 'New York'})
        jobs = Job.objects.filter(company__location__icontains='New York', is_available=True)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_search_job_with_title_and_location_filters(self):
        response = self.client.get(self.url, {'title': 'engineer', 'location': 'New York'})
        jobs = Job.objects.filter(title__icontains='engineer', company__location__icontains='New York', is_available=True)
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)





class LastJobsAPITest(APITestCase ):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('search-job-api')  



    def test_last_jobs_api(self):
        response = self.client.get(self.url)
        jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
        serializer = JobSerializer(jobs, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_last_jobs_api_no_available_jobs(self):
    
        Job.objects.all().update(is_available=False)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

   


