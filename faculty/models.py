from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import USER_TYPE_CHOICES, USER_STATUS_CHOICES, MAX_CLASSROOM_SIZE
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True,
                                 verbose_name=_("User Type"))
    is_authorized = models.BooleanField(default=False, verbose_name=_("Is Authorized"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_type', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_student(self):
        return self.user_type == 'student'

    def is_lecturer(self):
        return self.user_type == 'lecturer'

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    syllabus = models.FileField(upload_to='syllabus/', verbose_name=_("Syllabus"), blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')


class Faculty(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    subjects = models.ManyToManyField(Subject, related_name="faculty", verbose_name=_("Subjects"))
    lectures = models.ManyToManyField(CustomUser, related_name="faculty",
                                      limit_choices_to={'user_type': 'lecturer'},
                                      verbose_name=_("Lecturers"))

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __str__(self):
        return self.name



class Classroom(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subjects"))
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 limit_choices_to={'user_type': 'lecturer'}, verbose_name=_("Lecturers"))
    is_full = models.BooleanField(default=False, verbose_name=_("Is Full"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    max_students = models.IntegerField(verbose_name=_("Max Students"), default=MAX_CLASSROOM_SIZE)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')

    def __str__(self):
        return f'{self.subject} {self.lecturer}'


class SudentFaculty(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                limit_choices_to={'user_type': 'student'}, verbose_name=_("Student"))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty"))
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES, default='inactive',
                              verbose_name=_("User Type"))

    class Meta:
        verbose_name = _('Student Faculty')
        verbose_name_plural = _('Student Faculties')

    def __str__(self):
        return f"{self.student}: {self.faculty}"


# class LectureSubject(models.Model):
#     lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Lecturer"))
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subjects"))
#     has_permission = models.BooleanField(default=False, verbose_name=_("Has Permission"))
#
#     class Meta:
#         verbose_name = _('Lecture Subject')
#         verbose_name_plural = _('Lecture Subjects')


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                limit_choices_to={'user_type': 'student'}, verbose_name=_("Student"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_("Subject"))

    class Meta:
        verbose_name = _('Student Subject')
        verbose_name_plural = _('Student Subjects')

    def __str__(self):
        return f"{self.student}: {self.classroom}"
