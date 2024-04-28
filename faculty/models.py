from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.conf import settings

from faculty.choices import USER_TYPE_CHOICES, USER_STATUS_CHOICES, MAX_CLASSROOM_SIZE, DEFAULT_NUMBER_OF_CLASSES,\
    DEFAULT_LECTURE_DURATION
from django.utils.translation import gettext_lazy as _
from faculty.managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, blank=True, null=True,
                                 verbose_name=_("User Type"))
    is_authorized = models.BooleanField(default=True if settings.DEBUG else False, verbose_name=_("Is Authorized"))

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['user_type', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return " ".join([self.first_name, self.last_name])

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
    students = models.ManyToManyField(CustomUser, related_name="classrooms", limit_choices_to={'user_type': 'student'},
                                      verbose_name=_("Students"))
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name=_("Subjects"))
    lecturer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 limit_choices_to={'user_type': 'lecturer'}, verbose_name=_("Lecturers"))
    is_full = models.BooleanField(default=False, verbose_name=_("Is Full"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    max_students = models.IntegerField(verbose_name=_("Max Students"), default=MAX_CLASSROOM_SIZE)
    syllabus = models.FileField(upload_to='syllabus/', verbose_name=_("Syllabus"), blank=True, null=True)
    number_of_classes = models.IntegerField(verbose_name=_("Number of Classes"), default=DEFAULT_NUMBER_OF_CLASSES)

    class Meta:
        verbose_name = _('Classroom')
        verbose_name_plural = _('Classrooms')

    def __str__(self):
        return f'{self.subject} {self.lecturer}'


class Homework(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.TextField(verbose_name=_('Description'))
    due_date = models.DateTimeField(default=timezone.now, verbose_name=_('Due_date'))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_('Classroom'))
    is_active = models.BooleanField(verbose_name=_('Is_Active'), default=True)

    class Meta:
        verbose_name = _('Homework')
        verbose_name_plural = _('Homeworks')

    def __str__(self):
        return self.title


class StudentHomework(models.Model):
    student = models.ForeignKey(CustomUser, related_name="homework",
                                on_delete=models.CASCADE, verbose_name=_('Student'))
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, verbose_name=_('Homework'))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_('Classroom'))
    homework_text = models.TextField(blank=True, null=True, default=None, verbose_name=_('Homework_text'))
    homework_url = models.URLField(max_length=200, verbose_name=_('Homework URL'))


class StudentFaculty(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                limit_choices_to={'user_type': 'student'}, verbose_name=_("Student"))
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name=_("Faculty"))
    status = models.CharField(max_length=10, choices=USER_STATUS_CHOICES,
                              default='inactive' if not settings.DEBUG else 'active',
                              verbose_name=_("User Type"))

    class Meta:
        verbose_name = _('Student Faculty')
        verbose_name_plural = _('Student Faculties')

    def __str__(self):
        return f"{self.student}: {self.faculty} >> {self.status}"


class ClassroomCalendar(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="calendar", verbose_name=_("Classroom"))
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    duration = models.IntegerField(verbose_name=_("Duration"), default=DEFAULT_LECTURE_DURATION)

    class Meta:
        verbose_name = _('Classroom Calendar')
        verbose_name_plural = _('Classroom Calendars')

    def __str__(self):
        return f"{self.classroom}: {self.date} {self.start_time} - {self.duration}Hours"


class ClassroomAttendance(models.Model):
    classroom_date = models.ForeignKey(ClassroomCalendar, related_name="attendance", on_delete=models.CASCADE,
                                       verbose_name=_("Classroom"))
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendance",
                                limit_choices_to={'user_type': 'student'}, verbose_name=_("Student"))
    status = models.BooleanField(default=False, verbose_name=_("Status"))

    class Meta:
        verbose_name = _('Classroom Attendance')
        verbose_name_plural = _('Classroom Attendances')

    def __str__(self):
        return f"{self.classroom_date}"


class StudentSubject(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                limit_choices_to={'user_type': 'student'}, verbose_name=_("Student"))
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name=_("Subject"))

    class Meta:
        verbose_name = _('Student Subject')
        verbose_name_plural = _('Student Subjects')

    def __str__(self):
        return f"{self.student}: {self.classroom}"
