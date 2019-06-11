from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# Register your models here.
from .models import Student, Attendance, State, Local_govt

class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 1
class StudentAdmin(ImportExportModelAdmin):
    model = Student
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