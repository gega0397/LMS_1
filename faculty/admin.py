from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Subject, Faculty, Classroom, StudentSubject, StudentFaculty


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", 'user_type', 'first_name', 'last_name', 'is_authorized']
    ordering = ['date_joined']

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


@admin.register(StudentFaculty)
class StudentFacultyAdmin(admin.ModelAdmin):
    pass
