from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase , APIClient
from rest_framework import status
from .models import Job
from job.models import Job , Industry , ApplyJob
from company.models import Company
from users.models import User
from resume.models import Resume
from .serializers import JobSerializer , ResumeSerializer , ApplyJobSerializer
from .form import UpdateJobForm


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
    
    def test_company_jobs_api_with_valid_permissions(self):
        
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
                
        job_data1 = response.data[0]
        self.assertEqual(job_data1['id'], self.job1.id)
        self.assertEqual(job_data1['title'], self.job1.title)
        self.assertEqual(job_data1['description'], self.job1.description)
        
        
        job_data2 = response.data[1]
        self.assertEqual(job_data2['id'], self.job2.id)
        self.assertEqual(job_data2['title'], self.job2.title)
        self.assertEqual(job_data2['description'], self.job2.description)


    def test_company_jobs_api_without_permissions(self):

        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.url)

        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)





class JobResumesAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user3 = User.objects.create(username = 'gmail3@main.com' , email='gmail3@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')

        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        #self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry2 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        
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

    def test_job_resumes_api_success(self):
        
        url = reverse('job-resumes-api', args=[self.job1.pk])

        
        response = self.client.get(url)

        # Check the response status code and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('job', response.data)
        self.assertIn('resumes', response.data)
        self.assertEqual(response.data['job']['title'], self.job1.title)
        self.assertEqual(len(response.data['resumes']), 2)
        self.assertEqual(response.data['resumes'][0]['id'], self.resume1.id)
        self.assertEqual(response.data['resumes'][1]['id'], self.resume2.id)

    def test_job_resumes_api_job_not_found(self):
       
        non_existent_pk = 999

        
        url = reverse('job-resumes-api', args=[non_existent_pk])

        
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Job not found.')


class SpecificResumeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user3 = User.objects.create(username = 'gmail3@main.com' , email='gmail3@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')

        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        #self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry2 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        
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
        
        self.apply_job = ApplyJob.objects.create(job=self.job1, user = self.user1 , status = 'Accepted')

    def test_specific_resume_api_success(self):
        
        url = reverse('specific-resume-api', args=[self.job1.id, self.resume1.user])

        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('job', response.data)
        self.assertIn('resume', response.data)
        self.assertEqual(response.data['job']['title'], self.job1.title)
        self.assertEqual(response.data['resume']['user_id'], self.resume1.user)

    def test_specific_resume_api_resume_not_found(self):
       
        non_existent_user_id = 999

        
        url = reverse('specific-resume-api', args=[self.job1.id, non_existent_user_id])

        
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Resume not found for the specified job.')

    def test_specific_resume_api_apply_job_not_found(self):
        
        resume_without_apply_job = Resume.objects.create(user_id=2, name='Jane Smith')

        
        url = reverse('specific-resume-api', args=[self.job1.id, self.resume2.user])

        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Resume not found for the specified job.')



class UpdateApplyJobStatusAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user3 = User.objects.create(username = 'gmail3@main.com' , email='gmail3@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')

        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        #self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry2 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        
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
        
        self.apply_job = ApplyJob.objects.create(job=self.job1, user = self.user1 , status = 'Pending')

    def test_update_applyjob_status_api_success(self):
        
        url = reverse('update-applyjob-status-api', args=[self.job1.id, self.user1.id])

        
        new_status = 'Accepted'

        
        response = self.client.put(url, {'status': new_status}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.apply_job.id)
        self.assertEqual(response.data['job'], self.job1.id)
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertEqual(response.data['status'], new_status)

        
        updated_apply_job = ApplyJob.objects.get(id=self.apply_job.id)
        self.assertEqual(updated_apply_job.status, new_status)

    def test_update_applyjob_status_api_applyjob_not_found(self):
        
        non_existent_job_id = 999
        non_existent_user_id = 999

        
        url = reverse('update-applyjob-status-api', args=[non_existent_job_id, non_existent_user_id])

        
        response = self.client.put(url, {'status': 'Accepted'}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'ApplyJob not found.')



class AppliedJobsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user3 = User.objects.create(username = 'gmail3@main.com' , email='gmail3@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        
        self.industry1 = Industry.objects.create(name = 'industry1')
        self.industry2 = Industry.objects.create(name = 'industry2')

        self.company1 = Company.objects.create(user = self.user2 ,industry = self.industry1 , website = 'www.company1.com', about = 'good company',location = 'Tehran',size = '50-100', name='Company A')
        #self.company2 = Company.objects.create(user = self.user4 ,industry = self.industry2 , website = 'www.company2.com', about = 'very good company',location = 'Shiraz',size = '10-50', name='Company B')
        
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
        self.apply_job1 = ApplyJob.objects.create(job=self.job1, user = self.user1 , status = 'Applied')
        self.apply_job2 = ApplyJob.objects.create(job=self.job2, user = self.user1 , status = 'Applied')


    def test_applied_jobs_api_authenticated_user(self):
        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)
        

        
        url = reverse('applied-jobs-api')

        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['apply_jobs']), 2)
        self.assertEqual(len(response.data['jobs']), 2)

        
        apply_jobs_serializer = ApplyJobSerializer([self.apply_job1, self.apply_job2], many=True)
        self.assertEqual(response.data['apply_jobs'], apply_jobs_serializer.data)

        
        jobs_serializer = JobSerializer([self.job1, self.job2], many=True)
        self.assertEqual(response.data['jobs'], jobs_serializer.data)

    def test_applied_jobs_api_unauthenticated_user(self):
        
        url = reverse('applied-jobs-api')

        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_applied_jobs_api_exception(self):
        
        self.client.force_login(self.user3)
        self.client.force_authenticate(user=self.user3)

        
        url = reverse('applied-jobs-api')

        
        ApplyJob.objects.all().delete()

        
        response = self.client.get(url)

        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['message'], 'Internal Server Error')




class UpdateJobAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

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


    def test_update_job_api_success(self):

        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)
        

        
        url = reverse('update-job-api', args=[self.job1.id])

        
        form_data = {'title': 'Updated Job Title'}

        
        response = self.client.post(url, form_data, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Your Job Ad is now updated.')

        
        updated_job = Job.objects.get(id=self.job1.id)
        self.assertEqual(updated_job.title, 'Updated Job Title')

    def test_update_job_api_not_recruiter(self):
        
        
        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)
        
        url = reverse('update-job-api', args=[self.job1.id])

        response = self.client.post(url, {'title': 'Updated Job Title'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'Permission denied.')

    def test_update_job_api_job_not_found(self):
        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)

        non_existent_job_id = 999

        
        url = reverse('update-job-api', args=[non_existent_job_id])

        
        response = self.client.post(url, {'title': 'Updated Job Title'}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Job not found.')

    def test_update_job_api_invalid_form_data(self):

        self.client.force_login(self.user2)
        self.client.force_authenticate(user=self.user2)

        
        url = reverse('update-job-api', args=[self.job1.id])

        
        response = self.client.post(url, {'title': ''}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Something went wrong.')
        self.assertIn('title', response.data['errors'])


class ApplyToJobAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create(username = 'gmail1@main.com' , email='gmail1@main.com',is_applicant=True , is_recruiter=False , has_company=False , has_resume=True)
        self.user2 = User.objects.create(username = 'gmail2@main.com' , email='gmail2@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
        self.user4 = User.objects.create(username = 'gmail4@main.com' , email='gmail4@main.com',is_applicant=False , is_recruiter=True , has_company=True , has_resume=False)
       
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



    def test_apply_to_job_api_success(self):

        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)

        
        url = reverse('apply-to-job-api', args=[self.job1.id])

        
        response = self.client.post(url, {}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'You have successfully applied! Please check your dashboard.')

        
        self.assertTrue(ApplyJob.objects.filter(user=self.user1, job=self.job1).exists())

    def test_apply_to_job_api_already_applied(self):
        
        ApplyJob.objects.create(user=self.user1, job=self.job1)
        
        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)

        
        url = reverse('apply-to-job-api', args=[self.job1.id])

        
        response = self.client.post(url, {}, format='json')

        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['message'], 'You already applied for this job.')

    def test_apply_to_job_api_job_not_found(self):

        self.client.force_login(self.user1)
        self.client.force_authenticate(user=self.user1)


       
        non_existent_job_id = 999

        url = reverse('apply-to-job-api', args=[non_existent_job_id])

        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], 'Job not found.')

    def test_apply_to_job_api_not_authenticated(self):
        
        url = reverse('apply-to-job-api', args=[self.job1.id])

        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Permission denied.')

    def test_apply_to_job_api_not_applicant(self):
        
        self.client.force_login(self.user4)
        self.client.force_authenticate(user=self.user4)

        url = reverse('apply-to-job-api', args=[self.job1.id])

        response = self.client.post(url, {}, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Permission denied.')
