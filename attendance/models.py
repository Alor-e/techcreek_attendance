from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.urls import reverse

# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Local_govt(models.Model):
    name = models.CharField(max_length=255)
    state = models.ForeignKey(State, on_delete=models.PROTECT, related_name='local_government' )

    def __str__(self):
        return self.name

class Student(models.Model):
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    middlename = models.CharField(max_length=50, null=True, blank=True)
    birthday = models.DateField(verbose_name='Date of Birth')

    GENDER_CHOICES=(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other'),
    )

    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    
    QUALIFICATION_CHOICES = (
        ('O Level', 'O Level'),
        ('Undergraduate', 'Undergraduate'),
        ('OND/HND', 'OND/HND'),
        ("Bachelor's Degree", "Bachelor's Degree"),
        ("Master's Degree", "Master's Degree"),
        ('Other', 'Other'),
    )
    
    edu_qualification = models.CharField('Educational Qualification',max_length=50, choices=QUALIFICATION_CHOICES)
   
    PROGRAMS_CHOICES = (
    ('Codegaminators', (
            ('Codegaminators - Animation', 'Animation'),
            ('Codegaminators - Coding', 'Coding'),
            ('Codegaminators - Database', 'Database'),
            ('Codegaminators - Game Development', 'Game Development'),
            ('Codegaminators - Hardware/Networking', 'Hardware/Networking'),
            ('Codegaminators - Photography', 'Photography'),
        )
    ),

    ('ICT and Digital Lifestyle', (
            ('ICT and Digi-Lifestyle 5:00pm', 'ICT and Digital Lifestyle - 5:00pm'),
            ('ICT and Digi-Lifestyle 6:30pm', 'ICT and Digital Lifestyle - 6:30pm'),
        )
    ),

    ('Digi-lifestyle for kids', (
            ('Digi-lifestyle for kids 9:00am', 'Digi-lifestyle for kids - 9:00am'),
            ('Digi-lifestyle for kids 1:00pm', 'Digi-lifestyle for kids - 1:00pm'),
        )
    ),
    
    ('DBA 500', (
            ('DBA 500', 'DBA 500'),
        )
    ),
    )
    
    program = models.CharField(max_length=50, choices=PROGRAMS_CHOICES)
    state_of_origin = models.ForeignKey(State, on_delete=models.PROTECT, related_name='student')
    
    local_govt = ChainedForeignKey(
        Local_govt,
        chained_field="state_of_origin",
        chained_model_field="state",
        show_all=False,
        auto_choose=True,
        sort=True,
        verbose_name='Local Government',
        blank=True,
        null=True
        )
    email = models.EmailField(max_length=254)
    phone_no = models.CharField('Phone Number',max_length=15)
    address = models.TextField()
    registration_date = models.DateTimeField( auto_now=False, auto_now_add=True)
    unique_id = models.CharField(max_length=15, unique=True, null=True, blank=True)
    roll_no = models.PositiveSmallIntegerField('Number of times present',null=True, blank=True, default=0)
    already_taken = models.BooleanField(default=False, null=False, blank=False)
    picture = models.ImageField(upload_to = 'media/', null=True, blank=True )


    def __str__(self):
        return "{0} {1}".format(self.surname, self.firstname)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})    

    def get_percentage(self):
        total = Attendance.objects.filter(linked_student=self).count()
        present = Attendance.objects.filter(linked_student=self, present_state=True).count()
        try:
            percent = round((present/total)*100, 2)
        except ZeroDivisionError:
            percent = 0
        return percent

    def total_days(self):
        total = Attendance.objects.filter(linked_student=self).count()
        return total

class Attendance(models.Model):
    date = models.DateField( auto_now=False, auto_now_add=False)
    linked_student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='attendance')
    present_state = models.BooleanField(default=False)
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name_plural = 'Attendance'
        ordering = ['date', 'linked_student']
        unique_together = ['date', 'linked_student']
    
    def __str__(self):
        return "{0} on {1}".format(self.linked_student, self.date)
