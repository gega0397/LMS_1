from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import USER_TYPE_CHOICES


# Create your models here.

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True)
    is_authorized = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def is_student(self):
        return self.user_type == 'student'

    def is_lecturer(self):
        return self.user_type == 'student'


class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    syllabus = models.FileField(upload_to='syllabus/')

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject)
    lectures = models.ManyToManyField(CustomUser)


class Classroom(models.Model):
    subjects = models.ManyToManyField(Subject)
    lecturer = models.ManyToManyField(CustomUser)


class SudentFaculty(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)


class LectureFaculty(models.Model):
    lecture = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    faculty = models.manyToManyField(Faculty)
    subjects = models.ManyToManyField(Subject)


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
