from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication.models.base import User

from common.choices import DEGREE_CHOICES, MARITAL_STATUS_CHOICES
from common.models import BaseModel


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
