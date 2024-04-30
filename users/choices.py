from django.db import models


class UserTypeChoices(models.IntegerChoices):
    STUDENT = 1, "Student"
    LECTURER = 2, "Lecturer"
    ADMIN = 3, "Admin"


class UserTypeChoicesForm(models.IntegerChoices):
    STUDENT = 1, "Student"
    LECTURER = 2, "Lecturer"
