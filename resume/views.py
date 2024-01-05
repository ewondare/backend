from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Resume
from users.models import User
from .form import UpdateResumeForm
# Create your views here.

def update_resume(request):
    resume = Resume.objects.get(user=request.user)
    if (request.method == 'POST'):
        form = UpdateResumeForm(request.POST , instance=resume)
        if form.is_valid():
            var = form.save(commit=False)
            user = User.objects.get(pk=request.user.id)
            user.has_resume = True
            user.save()
            var.save()
            messages.info(request, 'Your')
            
