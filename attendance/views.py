"""My view"""
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.views import generic
from .models import Student, Attendance, State, Local_govt
from background_task import background
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
import background_task
from attendance.forms import StudentRegistrationForm
from django.urls import reverse
from .forms import SearchForm, SearchForm2
from django.shortcuts import render
from datetime import date



@background(schedule=10)
def attendance_resetter():
    all = Student.objects.all()

    for ind in all:
        if ind.attendance.all().filter(date=datetime.date.today(), present_state=True):
            pass
        else:
            ind.already_taken = False
            ind.save()
            if date.today().weekday() == 0 or date.today().weekday() == 2 or date.today().weekday() == 4:
                s = Student.objects.filter(program__icontains='Codegaminators')
                for b in s:
                    try:
                        a = Attendance(date=datetime.date.today(), linked_student=b)
                        a.save()
                    except:
                        pass
                    
            elif date.today().weekday() == 0 or date.today().weekday() == 1 or date.today().weekday() == 2 or date.today().weekday() == 3 or date.today().weekday() == 4:
                s = Student.objects.filter(program__contains='ICT')
                e = Student.objects.filter(program__contains='kids')
                r = Student.objects.filter(program__contains='DBA 500')
                other = s|e|r
                for b in other:
                    try:
                        a = Attendance(date=datetime.date.today(), linked_student=b)
                        a.save()
                    except:
                        pass
                    
                    


def landing_page(request):
    new_years_2099 = datetime.datetime(2099, 5, 17)
    attendance_resetter(repeat=60, repeat_until=new_years_2099)
    return render(request, 'home.html')



@login_required
def take_attendance_search(request):
    return render(request, 'take_attendance.html')



@method_decorator(login_required, name='dispatch')
class StudentListView(generic.ListView):
   
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 3

    def get_queryset(self):
        filter_version = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        order_c = 'surname'
        if order=='Student ID':
            order_c='id'
        elif order=='Name':
            order_c='surname'
        elif order=='Registration Date':
            order_c='-registration_date'
        elif order=='Times Present':
            order_c='-roll_no'
        new_context = Student.objects.filter(
            program_version__icontains=filter_version
        ).order_by(order_c)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['versions'] = Student.objects.\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
        return context


@login_required
def statistics(request):
    total_number=Student.objects.all().count()
    female_num = Student.objects.filter(gender='female').count()
    male_num = Student.objects.filter(gender='male').count()
    cgm = Student.objects.filter(program__icontains='Codegaminators').count()
    ict = Student.objects.filter(program__contains='ICT').count()
    kids = Student.objects.filter(program__contains='kids').count()
    dba_500 = Student.objects.filter(program__contains='DBA 500').count()
    photography_num = Student.objects.filter(program__icontains='Photography').count()
    coding_num = Student.objects.filter(program__icontains='Coding').count()
    animation_num = Student.objects.filter(program__icontains='Animation').count()
    database_num = Student.objects.filter(program__icontains='Database').count()
    game_dev_num = Student.objects.filter(program__icontains='Game Development').count()
    hardware_num = Student.objects.filter(program__icontains='Hardware/Networking').count()
    states = State.objects.all()
    lga = Local_govt.objects.filter(state_id=1)

    context = {'total_number':total_number,
               'female_num':female_num,
               'male_num':male_num,
               'cgm':cgm,
               'ict':ict,
               'kids':kids,
               'dba_500':dba_500,
               'photography_num':photography_num,
               'coding_num':coding_num,
               'animation_num':animation_num,
               'database_num':database_num,
               'game_dev_num':game_dev_num,
               'hardware_num':hardware_num,
               'states':states,
               'lga':lga}
    return render(request, 'statistics.html', context)



@method_decorator(login_required, name='dispatch')
class StudentCreateView( CreateView):
    model = Student
    form_class = StudentRegistrationForm
    template_name = 'student_registration.html'
    
    def get_success_url(self):
        return reverse('student_detail', kwargs={'pk': self.object.pk})
  


@method_decorator(login_required, name='dispatch')
class StudentDetailView(generic.DetailView):
    model = Student    
    template_name = 'student_detail.html'
    context_object_name = 'student'



@login_required
def registration_complete(request, pk):
    identity = get_object_or_404(Student, pk=pk)
    context = {'identity':identity}
    return render(request, 'student_reg_complete.html', context) 



@login_required
def search(request):
    form = SearchForm(request.GET or {})
    if form.is_valid() and form.has_changed():
        student_list = form.get_queryset()
    else:
        student_list = Student.objects.none()
    context= {'form':form, 'student_list':student_list}
    return render(request, 'search.html', context)



@login_required
def take_attendance_search2(request):
    form = SearchForm2(request.GET or {}, )
    if form.is_valid() and form.has_changed():
        student_list = form.get_queryset()
    else:
        student_list = Student.objects.none()
    context= {'form':form, 'student_list':student_list}   
    return render(request, 'search.html',context)



def take_attendance(request, pk):
    s = get_object_or_404(Student, pk=pk)
    '''print(s.__class__.objects.filter(attendance__date=datetime.date.today()))'''
    '''now = datetime.datetime.now()
    if now.hour == 13 and now.minute == 30:
        s.already_taken = False'''
    try:
        a = get_object_or_404(Attendance, date=datetime.date.today(), linked_student=s)
        a.present_state = True
        a.save()
        s.roll_no = Attendance.objects.filter(linked_student=s, present_state=True).count()
        s.already_taken = True
        s.save()
    except:
        a = Attendance(date=datetime.date.today(), linked_student=s)
        a.present_state = True
        a.save()
        s.roll_no = Attendance.objects.filter(linked_student=s, present_state=True).count()
        s.already_taken = True
        s.save()
        pass
    
    return HttpResponseRedirect(reverse('take_attendance_search'))




@login_required
def attendance_stats_cgm(request):
    
    a = Attendance.objects.filter(linked_student__program__contains='Codegaminators').order_by('date').values('date').distinct()
    
    total = a.count()
    filter_version = request.GET.get('filter', '')
    order = request.GET.get('orderby', '')
    order_c = 'surname'
    if order=='Student ID':
        order_c='id'
    elif order=='Name':
        order_c='surname'
    elif order=='Registration Date':
        order_c='-registration_date'
    elif order=='Times Present':
       order_c='-roll_no'
    student = Student.objects.filter(program__icontains='Codegaminators', program_version__icontains=filter_version ).order_by(order_c)
    versions = Student.objects.filter(program__icontains='Codegaminators').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
    context = {'a':a, 'student':student, 'total':total, 'versions':versions}
    return render(request, 'sp_table.html',context)

@login_required
def attendance_stats_ict(request):
    a = Attendance.objects.filter(linked_student__program__contains='ICT').order_by('date').values('date').distinct()
    total = a.count()
    filter_version = request.GET.get('filter', '')
    order = request.GET.get('orderby', '')
    order_c = 'surname'
    if order=='Student ID':
        order_c='id'
    elif order=='Name':
        order_c='surname'
    elif order=='Registration Date':
        order_c='-registration_date'
    elif order=='Times Present':
       order_c='-roll_no'
    student = Student.objects.filter(program__contains='ICT', program_version__icontains=filter_version ).order_by(order_c)
    versions = Student.objects.filter(program__icontains='ICT').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
    context = {'a':a, 'student':student, 'total':total, 'versions':versions}
    return render(request, 'sp_table.html',context)

@login_required
def attendance_stats_kids(request):
    a = Attendance.objects.filter(linked_student__program__contains='kids').order_by('date').values('date').distinct()
    total = a.count()
    filter_version = request.GET.get('filter', '')
    order = request.GET.get('orderby', '')
    order_c = 'surname'
    if order=='Student ID':
        order_c='id'
    elif order=='Name':
        order_c='surname'
    elif order=='Registration Date':
        order_c='-registration_date'
    elif order=='Times Present':
       order_c='-roll_no'
    student = Student.objects.filter(program__contains='kids', program_version__icontains=filter_version ).order_by(order_c)
    versions = Student.objects.filter(program__icontains='kids').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
    context = {'a':a, 'student':student, 'total':total, 'versions':versions}
    return render(request, 'sp_table.html',context)

@login_required
def attendance_stats_dba(request):
    a = Attendance.objects.filter(linked_student__program__contains='DBA 500').order_by('date').values('date').distinct()
    total = a.count()
    filter_version = request.GET.get('filter', '')
    order = request.GET.get('orderby', '')
    order_c = 'surname'
    if order=='Student ID':
        order_c='id'
    elif order=='Name':
        order_c='surname'
    elif order=='Registration Date':
        order_c='-registration_date'
    elif order=='Times Present':
       order_c='-roll_no'
    student = Student.objects.filter(program__contains='DBA 500', program_version__icontains=filter_version ).order_by(order_c)
    versions = Student.objects.filter(program__icontains='DBA 500').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
    context = {'a':a, 'student':student, 'total':total, 'versions':versions}
    return render(request, 'sp_table.html',context)




@method_decorator(login_required, name='dispatch')
class StudentListView_program_filter1(generic.ListView):
    queryset = Student.objects.filter(program__icontains='Codegaminators')
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 25

    def get_queryset(self):
        filter_version = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        order_c = 'surname'
        if order=='Student ID':
            order_c='id'
        elif order=='Name':
            order_c='surname'
        elif order=='Registration Date':
            order_c='-registration_date'
        elif order=='Times Present':
            order_c='-roll_no'
        new_context = Student.objects.filter(program__icontains='Codegaminators',
            program_version__icontains=filter_version
        ).order_by(order_c)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StudentListView_program_filter1, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['versions'] = Student.objects.filter(program__icontains='Codegaminators').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
        return context

@method_decorator(login_required, name='dispatch')
class StudentListView_program_filter2(generic.ListView):
    queryset = Student.objects.filter(program__icontains='ICT')
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 25

    def get_queryset(self):
        filter_version = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        order_c = 'surname'
        if order=='Student ID':
            order_c='id'
        elif order=='Name':
            order_c='surname'
        elif order=='Registration Date':
            order_c='-registration_date'
        elif order=='Times Present':
            order_c='-roll_no'
        new_context = Student.objects.filter(program__icontains='ICT',
            program_version__icontains=filter_version
        ).order_by(order_c)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StudentListView_program_filter2, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['versions'] = Student.objects.filter(program__icontains='ICT').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
        return context

@method_decorator(login_required, name='dispatch')
class StudentListView_program_filter3(generic.ListView):
    queryset = Student.objects.filter(program__icontains='kids')
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 25

    def get_queryset(self):
        filter_version = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        order_c = 'surname'
        if order=='Student ID':
            order_c='id'
        elif order=='Name':
            order_c='surname'
        elif order=='Registration Date':
            order_c='-registration_date'
        elif order=='Times Present':
            order_c='-roll_no'
        new_context = Student.objects.filter(program__icontains='kids',
            program_version__icontains=filter_version
        ).order_by(order_c)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StudentListView_program_filter3, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['versions'] = Student.objects.filter(program__icontains='kids').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
        return context

class StudentListView_program_filter4(generic.ListView):
    queryset = Student.objects.filter(program__contains='DBA 500')
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 25

    def get_queryset(self):
        filter_version = self.request.GET.get('filter', '')
        order = self.request.GET.get('orderby', '')
        order_c = 'surname'
        if order=='Student ID':
            order_c='id'
        elif order=='Name':
            order_c='surname'
        elif order=='Registration Date':
            order_c='-registration_date'
        elif order=='Times Present':
            order_c='-roll_no'
        new_context = Student.objects.filter(program__contains='DBA 500',
            program_version__icontains=filter_version
        ).order_by(order_c)
        return new_context

    def get_context_data(self, **kwargs):
        context = super(StudentListView_program_filter4, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        context['orderby'] = self.request.GET.get('orderby', '')
        context['versions'] = Student.objects.filter(program__icontains='DBA 500').\
            	exclude(program_version__isnull=True).exclude(program_version__exact='').\
            	order_by('program_version').values('program_version').distinct()
        return context

