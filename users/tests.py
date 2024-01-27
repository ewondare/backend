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


    def test_register_applicant_success(self):
        
        payload = {
            'email': 'test1@gmail.com',
            'password1': '3405934klfjas',
            'password2':'3405934klfjas',
            'username' : 'test1@gmail.com',
            'is_applicant' : True
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Your account has been created successfully.')
        self.assertIn('userid', response.data)
        self.assertIn('token', response.data)

        user = User.objects.get(email=payload['email'])
        self.assertEqual(user.username, payload['username'])
        self.assertTrue(user.is_applicant)
        self.assertEqual(user.resume.user, user)

    def test_register_applicant_duplicate_email(self):

        payload = {
            'email': 'gmail1@main.com',
            'password1': '40981oidaflkj',
            'password2': '40981oidaflkj'
        }

        response = self.client.post(self.url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'A user with the same email or username already exists.')


    def test_register_applicant_api_invalid_data(self):
        
        payload = {
            'email': 'test1@gmail.com',
            'password1': '3405934klfjas',
            'password2':'9401i2lsakdf',
            'username' : 'test1@gmail.com',
            'is_applicant' : True
        }

        
        response = self.client.post(self.url, payload , format='json')

        self.assertEqual(response.status_code, 400)


class RegisterRecruiterAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('register-recruiter-api')
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)

    def test_register_recruiter_success(self):
        
        payload = {
            'email': 'test1@example.com',
            'password1': '241t4kgalsm',
            'password2': '241t4kgalsm',
            'username' : 'test1@example.com',
            'is_recruiter' : True
        }

        response = self.client.post(self.url, payload, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Your account has been created successfully.')
        self.assertIn('userid', response.data)
        self.assertIn('token', response.data)

        
        user = User.objects.get(email=payload['email'])
        self.assertEqual(user.username, payload['username'])
        self.assertTrue(user.is_recruiter)
        self.assertEqual(user.company.user, user)

    def test_register_recruiter_duplicate_email(self):
    
        
        payload = {
            'email': 'gmail2@main.com',
            'password1': '241t4kgalsm',
            'password2': '241t4kgalsm',
            'username' : 'gmail2@main.com',
            'is_recruiter' : True
        }

        
        response = self.client.post(self.url, payload, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'A user with the same email or username already exists.')

    def test_register_recruiter_api_invalid_data(self):
        
        payload = {
            'email': 'test1@gmail.com',
            'password1': '3405934klfjas',
            'password2':'24t4tsasdlasda',
            'username' : 'test1@gmail.com',
        }

        
        response = self.client.post(self.url, payload , format='json')

        self.assertEqual(response.status_code, 400)


class LoginUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login-user-api')

        self.user1 = User.objects.create(username = 'gmail1@main.com' ,password = '98328923lksdfa', email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=False)

    def test_login_user_invalid_credentials(self):
        
        payload = {
            'email': 'gmail1@main.com',
            'password': '12323489fj',
        }

        
        response = self.client.post(self.url, payload, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid credentials. Please try again.')

class LogoutUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create(username = 'gmail1@main.com' ,password = '98328923lksdfa', email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=False)
        
        self.url = reverse('logout-user-api')

        self.client.force_authenticate(user=self.user1)

    def test_logout_user(self):
        response = self.client.post(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Successfully logged out.')