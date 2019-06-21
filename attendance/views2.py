from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import StudentSerializers
from .models import Student
from .pagination import StandardResultsSetPagination
from attendance.forms import MyForm

def StudentList(request):
    total_number=Student.objects.all().count()
    

    context = {'total_number':total_number}

    return render(request, "Student_Statistics.html", context)

class StudentListing(ListAPIView):

    pagination_class = StandardResultsSetPagination
    serializer_class = StudentSerializers

    def get_queryset(self):
        
        queryList = Student.objects.all()
        
        program = self.request.query_params.get('program', None)
        state_of_origin = self.request.query_params.get('state_of_origin', None)
        program_version = self.request.query_params.get('program_version', None)
        local_govt = self.request.query_params.get('local_govt', None)
        program_specific = self.request.query_params.get('program_specific', None)
        sort_by = self.request.query_params.get('sort_by', None)

        if program:
            queryList = queryList.filter(program = program)
        if state_of_origin:
            queryList = queryList.filter(state_of_origin = state_of_origin)
        if program_version:
            queryList = queryList.filter(program_version = program_version)
        if local_govt:
            queryList = queryList.filter(local_govt = local_govt)
        if program_specific:
            queryList = queryList.filter(program_specific = program_specific)
        
        if sort_by == "unique_id":
            queryList = queryList.order_by("unique_id")
        elif sort_by == "registration_date":
            queryList = queryList.order_by("registration_date")
        elif sort_by == "roll_no":
            queryList = queryList.order_by("roll_no")

        return queryList


def get_program(request):
    
    if request.method == "GET" and request.is_ajax():
        program = Student.objects.exclude(program__isnull=True).\
            exclude(program__exact='').order_by('program').values_list('program').distinct()
        program = [i[0] for i in list(program)]
        data = {
            "program": program, 
        }
        return JsonResponse(data, status = 200)


def get_state_of_origin(request):
    if request.method == "GET" and request.is_ajax():

        state_of_origin = Student.objects.exclude(state_of_origin__isnull=True).\
        	exclude(state_of_origin__exact='').order_by('state_of_origin').values_list('state_of_origin').distinct()
        state_of_origin = [i[0] for i in list(state_of_origin)]
        data = {
            "state_of_origin": state_of_origin, 
        }
        return JsonResponse(data, status = 200)


def get_program_version(request):
    

    if request.method == "GET" and request.is_ajax():
        program = request.GET.get('program')
        program_version = Student.objects.filter(program = program).\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values_list('program_version').distinct()
        program_version = [i[0] for i in list(program_version)]
        data = {
            "program_version": program_version, 
        }
        return JsonResponse(data, status = 200)


def get_local_govt(request):
    

    if request.method == "GET" and request.is_ajax():
        state_of_origin = request.GET.get('state_of_origin')
        local_govt = Student.objects.filter(state_of_origin = state_of_origin).\
            	exclude(local_govt__isnull=True).exclude(local_govt__exact='').\
            	order_by('local_govt').values_list('local_govt').distinct()
        local_govt = [i[0] for i in list(local_govt)]
        data = {
            "local_govt": local_govt, 
        }
        return JsonResponse(data, status = 200)


def get_program_specific(request):
    

    if request.method == "GET" and request.is_ajax():
        program = request.GET.get('program')
        program_specific = Student.objects.filter(program = program).\
            	exclude(program_specific__isnull=True).exclude(program_specific__exact='').\
            	order_by('program_specific').values_list('program_specific').distinct()
        program_specific = [i[0] for i in list(program_specific)]
        data = {
            "program_specific": program_specific, 
        }
        return JsonResponse(data, status = 200)



from django.http import HttpResponse 
from django.shortcuts import render, redirect 
from .forms import MyForm
from django.views.decorators.csrf import csrf_exempt  
# Create your views here. 
def take_image(request): 
    return render(request, "student_registration_image.html")

@csrf_exempt  
def save_image(request, pk): 
    if request.method == 'POST':
        passfile = request.FILES.get('file')
        s = Student.objects.get(pk=pk)
        s.picture = passfile
        s.save()
        return HttpResponse('image upload success')
    return render(request, "student_registration_image.html")