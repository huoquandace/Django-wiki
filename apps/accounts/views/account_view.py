
from django import forms
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView, 
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.views.generic import FormView, TemplateView, View
from django.utils.translation import gettext_lazy as _

from accounts.models.profile_model import Profile


class Register(FormView):

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

    template_name = 'auth/register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        new_user = get_user_model().objects.create_user(
            username = data['username'],
            password = data['password1'],
            email = data['email'],
        )
        url = f"{reverse('register_done')}?username={new_user.username}"
        return redirect(url)


class RegisterDone(TemplateView):
    template_name = 'auth/register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'


class ProfileUpdateView(LoginRequiredMixin, View):
    
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['gender', 'phone', 'age', 'birthday', 'avatar' ,'address',]

    class UserForm(forms.ModelForm):
        username = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
        class Meta:
            model = get_user_model()
            fields = ('username', 'email', 'first_name', 'last_name')

    def get(self, request):
        profile_form = self.ProfileForm(instance=request.user.profile)
        user_form = self.UserForm(instance=request.user)
        context = {
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'auth/profile_update.html', context)
    
    def post(self, request):
        user_form = self.UserForm(request.POST, instance=request.user)
        profile_form = self.ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'errors')
            return redirect('profile_update')


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = 'auth/password_change_form.html'
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'


class PasswordReset(PasswordResetView):
    template_name = 'auth/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')
    from_email = 'system@sys.com'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'


