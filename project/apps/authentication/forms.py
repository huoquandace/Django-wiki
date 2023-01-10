from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from authentication.models import Profile


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'required': True
                }
            )
        }


class AuthForm(AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("UR CUSTOM MESSAGE"),
    }

    def confirm_login_allowed(self, user):
        # return
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
        if user.username.startswith('b'):
            raise ValidationError(
                _("Sorry, accounts starting with 'b' aren't welcome here."),
                code='no_b_users',
            )


class ProfileUpdateForm(forms.ModelForm):
    email = forms.CharField(max_length=100)
    class Meta:
        model = Profile
        fields = '__all__'

        