from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse

from rest_framework.test import APIClient , APITestCase
from rest_framework import status
from job.models import Job , Industry , ApplyJob
from company.models import Company


from users.models import User
from resume.models import Resume




class RegisterApplicantAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.url = reverse('register-applicant-api')  
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
'''
    def test_register_applicant_api_success(self):
        # Create a valid request data
        data = {
            'email': 'gmail1@main.com',
            'password1': 'password',
            'password2': 'password'
            # Include other required fields in the data
        }

        # Send a POST request to the API
        response = self.client.post(self.url, data)

        # Check the response status code and data
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Your account has been created successfully.')

        # Check if the user is created in the database
        user = User.objects.get(email='gmail1@main.com')
        self.assertEqual(user.is_applicant, True)
        # Add more assertions for other user attributes if needed

        # Check if a resume is created for the user
        self.assertTrue(Resume.objects.filter(user=user).exists())


        # Check if the response contains the user ID and token
        self.assertEqual(response.data['userid'], user.id)
        # Add assertions for the token if needed

    def test_register_applicant_api_duplicate_email(self):
        # Create an existing user with the same email
        User.objects.create(email='test@example.com', password='password')

        # Create a request data with the duplicate email
        data = {
            'email': 'test@example.com',
            'password': 'password',
            # Include other required fields in the data
        }

        # Send a POST request to the API
        response = self.client.post(self.url, data)

        # Check the response status code and data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['message'], 'A user with the same email or username already exists.')

    def test_register_applicant_api_invalid_data(self):
        # Create an invalid request data
        data = {
            # Missing required fields or invalid field values
        }

        # Send a POST request to the API
        response = self.client.post(self.url, data)

        # Check the response status code and data
        self.assertEqual(response.status_code, 400)
        # Add more assertions for the error message if needed
'''