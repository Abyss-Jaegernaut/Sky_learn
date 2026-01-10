from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.user_course_list, name='user_course_list'),
    path('course/<slug:slug>/', views.course_single, name='course_single'),
    path('course/<slug:slug>/edit/', views.edit_course, name='edit_course'),
    
    # Uploads
    path('course/<slug:slug>/upload-file/', views.upload_file_view, name='upload_file_view'),
    path('course/<slug:slug>/upload-video/', views.upload_video, name='upload_video'),
    path('course/<slug:slug>/file/<int:file_id>/edit/', views.upload_file_edit, name='upload_file_edit'),
    path('course/<slug:slug>/file/<int:file_id>/delete/', views.upload_file_delete, name='upload_file_delete'),
    path('course/<slug:slug>/video/<slug:video_slug>/edit/', views.upload_video_edit, name='upload_video_edit'),
    path('course/<slug:slug>/video/<slug:video_slug>/delete/', views.upload_video_delete, name='upload_video_delete'),

    # Programs
    path('programs/', views.programs, name='programs'),
    path('program/add/', views.add_program, name='add_program'),
    path('program/<int:pk>/', views.program_detail, name='program_detail'),
    path('program/<int:pk>/edit/', views.edit_program, name='edit_program'),
    path('program/<int:pk>/delete/', views.program_delete, name='program_delete'),

    path('course/add/<slug:slug>/', views.course_add, name='course_add'),
    path('course/<slug:slug>/delete/', views.delete_course, name='delete_course'),
    path('projets/', views.mes_projets, name='mes_projets'),
    path('lecturers/', views.lecturer_list, name='lecturer_list'),
    path('lecturer/add/', views.add_lecturer, name='add_lecturer'),
    path('lecturer/<int:pk>/edit/', views.staff_edit, name='staff_edit'),
    path('lecturer/<int:pk>/delete/', views.lecturer_delete, name='lecturer_delete'),
    path('lecturer/list/pdf/', views.lecturer_list_pdf, name='lecturer_list_pdf'),

    path('students/', views.student_list, name='student_list'),
    path('student/add/', views.add_student, name='add_student'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('student/list/pdf/', views.student_list_pdf, name='student_list_pdf'),
    
    path('profile/<int:id>/', views.profile_single, name='profile_single'),
    path('profile/<int:id>/program/edit/', views.student_program_edit, name='student_program_edit'),
    path('course-allocation/', views.course_allocation_view, name='course_allocation_view'),
    path('sessions/', views.session_list, name='session_list'),
    path('session/add/', views.add_session, name='add_session'),
    path('session/<int:pk>/edit/', views.edit_session, name='edit_session'),
    path('session/<int:pk>/delete/', views.delete_session, name='delete_session'),
    path('semesters/', views.semester_list, name='semester_list'),
    path('add-score/', views.add_score, name='add_score'),
    path('grade-results/', views.grade_results, name='grade_results'),
    path('ass-results/', views.ass_results, name='ass_results'),
    path('course-registration/', views.course_registration, name='course_registration'),
    path('course-drop/', views.course_registration, name='course_drop'),
    path('course-registration-form/', views.course_registration, name='course_registration_form'),
    path('quiz-progress/', views.quiz_progress, name='quiz_progress'),
    path('quiz-marking/', views.quiz_marking, name='quiz_marking'),
    path('quiz/<slug:slug>/', views.quiz_index, name='quiz_index'),

    path('post/add/', views.add_post, name='add_item'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('query/', views.home, name='query'), # Placeholder for search
]
