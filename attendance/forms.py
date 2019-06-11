"""My forms"""

from django.forms import ModelForm, TextInput, EmailInput
from django import forms
from .models import Student
from simple_search import search_form_factory



class DateInputs(forms.DateInput):
    input_type = 'date'

class StudentRegistrationForm(ModelForm):
    
    class Meta:
        model = Student
        fields = ['surname', 'firstname', 'middlename', 'birthday', 'gender', 'edu_qualification', 'program', 'state_of_origin', 'local_govt', 'email', 'phone_no', 'address', 'picture']
        widgets = {
            'address': TextInput(attrs={ 'placeholder': 'e.g 20 Dave Street off Aba Road'}),
            'email': EmailInput(attrs={'placeholder': 'e.g john21@example.com'}),
            'phone_no': TextInput(attrs={'placeholder': 'e.g 08052220001'}),
            'birthday': DateInputs(),
            'middlename': TextInput(attrs={'placeholder': 'Optional'}),

            
        }




SearchForm = search_form_factory(Student.objects.all(),
                                 ['surname', 'firstname', 'middlename', 'program'])

SearchForm2 = search_form_factory(Student.objects.all(),
                                 ['=id'])
