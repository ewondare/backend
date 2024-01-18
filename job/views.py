from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Job, ApplyJob
from .form import CreateJobForm, UpdateJobForm

# Create your views here.


# create a job 
def create_job(request):
    if request.user.is_recruiter and request.user.has_company:
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                var.user = request.user
                var.company = request.user.company
                var.save()
                messages.info(request, 'New Job has been created.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong.')
                return redirect('create-job')
        else: 
            form = CreateJobForm()
            context = {'form':form}
            return render(request, 'job/create_job.html', context)
    else:
        messages.warning(request, 'Permission denied.')
        return redirect('dashboard')
        

# update a job 
def update_job(request, pk):
    if request.user.is_recruiter and request.user.has_company:
        job = Job.objects.get(pk=pk)
        if request.method == 'POST':
            form = UpdateJobForm(request.POST , instance=job)
            if form.is_valid():
                form.save()
                messages.info(request, 'Your JobAD is now updated.')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong.')
                return redirect('dashboard')
        else: 
            form = UpdateJobForm()
            context = {'form':form}
            return render(request, 'job/update_job.html', context)
    else:
        messages.warning(request, 'Permission denied.')
        return redirect('dashboard')
    

def manage_jobs(request):
    jobs = Job.objects.filter(user=request.user , company=request.user.company)
    context = {'jobs':jobs}
    return render(request, 'job/manage_jobs.html' , context)

def apply_to_job(request , pk):
    if request.user.is_authenticated:
        job = Job.objects.get(pk=pk)
        if ApplyJob.objects.filter(user=request.user , job=pk).exists():
            messages.warning(request, 'Permission Denied.')
            return redirect('dashboard')
        else:
            ApplyJob.objects.create(
                job=job,
                user = request.user,
                status = 'Pending'
            )
            messages.info(request, 'You have successfully applied! please see dashboard.')
            return redirect('dashboard')
    else:
        messages.info(request, 'Please Log In to continue.')
        return redirect('login')