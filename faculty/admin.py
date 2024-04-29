from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from faculty.forms import CustomUserCreationForm, CustomUserChangeForm
from faculty.models import CustomUser, Subject, Faculty, Classroom, StudentSubject, StudentFaculty, Homework


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", 'user_type', 'first_name', 'last_name', 'is_authorized']
    ordering = ['date_joined']
    list_filter = ['is_authorized', 'user_type']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_authorized', 'user_type',)}),
        ('Important dates', {'fields': ('last_login', 'date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name',
                'last_name', 'password1', 'password2',
                'is_authorized', 'user_type',),
        }),
    )


# admin.site.register(CustomUser, CustomUserAdmin)


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
