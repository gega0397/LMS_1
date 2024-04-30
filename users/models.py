from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from users.managers import CustomUserManager
from users.choices import UserTypeChoices


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    user_type = models.CharField(max_length=10, choices=UserTypeChoices, blank=True, null=True,
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
