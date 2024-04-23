from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Subject, Faculty, Classroom, StudentSubject


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", 'user_type', 'first_name', 'last_name', 'is_authorized']
    ordering = ['date_joined']


admin.site.register(CustomUser, CustomUserAdmin)


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
