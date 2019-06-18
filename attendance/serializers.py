from rest_framework import serializers
from .models import Student

class StudentSerializers(serializers.ModelSerializer):
	class Meta:
	    model = Student
	    fields = ('id', 'surname', 'firstname', 'middlename', 'unique_id', 'birthday', 'gender', 'edu_qualification', 'program', 'program_specific', 
		'state_of_origin', 'local_govt', 'email', 'phone_no', 'address', 'picture', 'roll_no', 'registration_date', 'program_version')