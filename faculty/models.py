from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import USER_TYPE_CHOICES
from django.utils.translation import gettext_lazy as _


# Create your models here.

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True,verbose_name=_("User Type"))
    is_authorized = models.BooleanField(default=False, verbose_name=_("Is Authorized"))

    def __str__(self):
        return self.username

    def is_student(self):
        return self.user_type == 'student'

    def is_lecturer(self):
        return self.user_type == 'student'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    syllabus = models.FileField(upload_to='syllabus/', verbose_name=_("Syllabus"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    subjects = models.ManyToManyField(Subject, related_name="faculty", verbose_name=_("Subjects"))
    lectures = models.ManyToManyField(CustomUser, related_name="faculty", verbose_name=_("Lecturers"))

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

class Classroom(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subjects"))
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Lecturers"))

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')

class SudentFaculty(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Student"), unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty"))

    class Meta:
        verbose_name = _('Student Faculty')
        verbose_name_plural = _('Student Faculties')

class LectureSubject(models.Model):
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Lecturer"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subjects"))
    has_permission = models.BooleanField(default=False, verbose_name=_("Has Permission"))

    class Meta:
        verbose_name = _('Lecture Faculty')
        verbose_name_plural = _('Lecture Faculties')


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Student"))
    subject = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_("Subject"))

    class Meta:
        verbose_name = _('Student Subject')
        verbose_name_plural = _('Student Subjects')