from django.apps import AppConfig
from watson import search as watson_search

class AttendanceConfig(AppConfig):
    name = 'attendance'
    def ready(self):
        student_model  = self.get_model('Student' )
        watson_search.register(student_model, store=("surname", "firstname", "middlename", "id"))