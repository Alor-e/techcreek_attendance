from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Student, Attendance, State, Local_govt
from import_export import resources, fields

class StudentResource(resources.ModelResource):
    
    SN = fields.Field(column_name='S/N')
    firstname = fields.Field(attribute='firstname', column_name='Firstname')
    surname = fields.Field(attribute='surname', column_name='Surname')
    phone_no = fields.Field(attribute='phone_no', column_name='Phone')
    email = fields.Field(attribute='email', column_name='Email')
    program_specific = fields.Field(attribute='program_specific', column_name='Course')
    test_score = fields.Field(attribute='test_score', column_name='Test Score')
    birthday = fields.Field(attribute='birthday', column_name='DOB')
    edu_qualification = fields.Field(attribute='edu_qualification', column_name='Qualification')
    state_of_origin = fields.Field(attribute='state_of_origin', column_name='State')
    local_govt = fields.Field(attribute='local_govt', column_name='LGA')
    address = fields.Field(attribute='address', column_name='Address')

    class Meta:
        model = Student
        exclude = ('picture', 'already_taken' )

class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 1

class StudentAdmin(ImportExportModelAdmin):
    model = Student
    resource_class = StudentResource
    list_display = ('surname', 'firstname', 'unique_id', 'email', 'phone_no', 'registration_date')
    list_filter = ['registration_date']
    search_fields = ['unique_id', 'surname', 'firstname' ]
    inlines = [
        AttendanceInline,
    ]

class AttendanceAdmin(ImportExportModelAdmin):
    model = Attendance
    #list_display = ['link', 'state']


admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(State)
admin.site.register(Local_govt)