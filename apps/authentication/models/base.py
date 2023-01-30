from django.db import models
from django.contrib import auth
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(auth.models.AbstractBaseUser, auth.models.PermissionsMixin):
    username = models.CharField(_("username"), max_length=100, unique=True, validators=[auth.validators.UnicodeUsernameValidator()], error_messages={"unique": _("A user with that username already exists."),})
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("last name"), max_length=100, blank=True)    # Surname
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False,)
    is_active = models.BooleanField(_("active"), default=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = auth.models.UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        identifier = self.username
        try:
            if self.last_name != "" or self.first_name != "":
                identifier = f"{self.last_name} {self.first_name}"
        except:
            pass
        return identifier


class Profile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        UNKNOWN = 'U', _('Unknown')

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    gender = models.CharField(_("gender"), max_length=100, blank=True, choices=Gender.choices)
    phone = models.CharField(_("phone"), max_length=100, blank=True, null=True)
    age = models.IntegerField(_("age"), blank=True, null=True)
    address = models.TextField(_("address"), blank=True, null=True)
    birthday = models.DateField(_("birthday"), max_length=10, blank=True, null=True)
    avatar = models.ImageField(default='images/avatar_default1.jpg', upload_to='images')

    def __str__(self):
        return f"Profile of {self.user.username}"

    def save(self, *args, **kwargs):
        if self.gender == 'Female':
            self.avatar = 'images/avatar_default2.jpg'
        return super().save(*args, **kwargs)
