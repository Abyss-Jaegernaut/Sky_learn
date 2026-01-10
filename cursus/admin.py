from django.contrib import admin
from .models import Course, Module, Lesson, certificat, Projet, Post, Enrollment, Program, Session, Semester

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    search_fields = ('title',)

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('session', 'is_current_session', 'next_session_beginning')

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('semester', 'is_current_semester', 'session')
    list_filter = ('session',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('titre', 'code', 'instructeur', 'program', 'level', 'prix')
    list_filter = ('program', 'level', 'instructeur')
    search_fields = ('titre', 'code', 'description')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'course')
    list_filter = ('course',)
    search_fields = ('titre',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('titre', 'module')
    list_filter = ('module__course', 'module')
    search_fields = ('titre', 'contenu')

@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'course', 'utilisateur', 'date_rendu', 'score')
    list_filter = ('course', 'utilisateur')
    search_fields = ('titre', 'description')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type_post', 'updated_date')
    list_filter = ('type_post',)
    search_fields = ('titre', 'resume')

@admin.register(certificat)
class CertificatAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'course', 'date_obtention')
    list_filter = ('course',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date_enrolled')
    list_filter = ('course', 'student')
    search_fields = ('student__username', 'course__titre')