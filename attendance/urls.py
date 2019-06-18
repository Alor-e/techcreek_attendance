from django.urls import include, path
from . import views, views2

urlpatterns = [
    
    path('take_search/', views.take_attendance_search, name = 'take_attendance_search'),
    path('search_processing/', views.take_attendance_search2, name = 'take_attendance_search2'),
    path('registration/add/', views.StudentCreateView.as_view(), name = 'stu_registration'),
    path('student/', views.StudentListView.as_view(), name = 'student_list'),
    path('student_detail/<int:pk>', views.StudentDetailView.as_view(), name ='student_detail'),
    path('registration_complete/<int:pk>', views.registration_complete, name='reg_complete'),
    path('search/', views.search, name='search'),
    path('take/<int:pk>', views.take_attendance, name='take_attendance'),
    path('statistics/', views.statistics, name='statistics'),

    path('summary_cgm/', views.attendance_stats_cgm, name='cgm_summary'),
    path('summary_ict/', views.attendance_stats_ict, name='ict_summary'),
    path('summary_kids/', views.attendance_stats_kids, name='kids_summary'),
    path('summary_dba/', views.attendance_stats_dba, name='dba_summary'),

    path('student/order_by_name/', views.StudentListView_name_order.as_view(), name = 'student_list_name_order'),
    path('student/order_by_date/', views.StudentListView_date_order.as_view(), name = 'student_list_date_order'),
    path('student/order_by_present/', views.StudentListView_present_order.as_view(), name = 'student_list_present_order'),

    path('student/filter1', views.StudentListView_program_filter1.as_view(), name = 'student_list_program_filter1'),
    path('student/filter2', views.StudentListView_program_filter2.as_view(), name = 'student_list_program_filter2'),
    path('student/filter3', views.StudentListView_program_filter3.as_view(), name = 'student_list_program_filter3'),
    path('student/filter4', views.StudentListView_program_filter4.as_view(), name = 'student_list_program_filter4'),

    path('', views2.StudentList, name = 'attendance'),
    path("student_listing/", views2.StudentListing.as_view(), name = 'listing'),
    path("ajax/program/", views2.get_program, name = 'get_program'),
    path("ajax/state_of_origin/", views2.get_state_of_origin, name = 'get_state_of_origin'),
    path("ajax/program_version/", views2.get_program_version, name = 'get_program_version'),
    path("ajax/local_govt/", views2.get_local_govt, name = 'get_local_govt'),
    path("ajax/program_specific/", views2.get_program_specific, name = 'get_program_specific'),
]