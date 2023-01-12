from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from common.choices import DEGREE_CHOICES, MARITAL_STATUS_CHOICES
from common.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, unique=True, validators=[UnicodeUsernameValidator()], error_messages={"unique": _("A user with that username already exists."),})
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False,)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        identifier = self.username
        try:
            if self.profile.last_name != "" or self.profile.first_name != "":
                identifier = f"{self.profile.last_name} {self.profile.first_name}"
        except:
            pass
        return identifier

class Profile(BaseModel):

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNKNOWN = 'U', _('Unknown')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(_("gender"), max_length=100, blank=True, choices=Gender.choices)
    degree = models.CharField(_("degree"), max_length=100, blank=True, null=True, choices=DEGREE_CHOICES)
    marital_status = models.CharField(_("marital_status"), max_length=100, blank=True, null=True, choices=MARITAL_STATUS_CHOICES)

    avatar = models.ImageField(default='images/avatar_default1.jpg', upload_to='images')

    age = models.IntegerField(_("age"), blank=True, null=True)
    birthday = models.DateField(_("birthday"), max_length=10, blank=True, null=True)
    certificate = models.TextField(_("certificate"), blank=True, null=True)

    u_id = models.CharField(_("u_id"), max_length=100, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)    # Surname
    phone = models.CharField(_("phone"), max_length=100, blank=True, null=True)
    address = models.CharField(_("address"), max_length=100, blank=True, null=True)
    citizen_identification = models.CharField(_("citizen identification"), max_length=100, blank=True, null=True)
    tax_code = models.CharField(_("tax code"), max_length=100, blank=True, null=True)
    license_plates = models.CharField(_("license_plates"), max_length=100, blank=True, null=True,)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self, *args, **kwargs):
        if self.gender == 'Female':
            self.avatar = 'images/avatar_default2.jpg'
        return super().save(*args, **kwargs)
