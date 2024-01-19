import django_filters
from job.models import Job 

class Jobfilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Job
        fields = ['title' , 'location' , 'job_type' , 'industry']