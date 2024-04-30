from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from faculty.models import CustomUser, Subject, Faculty, Classroom, StudentSubject, StudentFaculty, Homework


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentSubject)
class StudentSubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentFaculty)
class StudentFacultyAdmin(admin.ModelAdmin):
    list_display = ['student', 'faculty', 'status']
    list_filter = ['status', 'faculty']


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'due_date']
