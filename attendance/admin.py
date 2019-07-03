from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Student, Attendance, State, Local_govt
from import_export import resources

class StudentResource(resources.ModelResource):

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