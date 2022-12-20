from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UsernameField


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email')
        field_classes = {'username': UsernameField}
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'required': True
                }
            )
        }