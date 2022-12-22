from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.utils.translation import gettext_lazy as _

from authentication.forms import RegisterForm, AuthForm


class Login(LoginView):
    authentication_form = AuthForm # Defauts to AuthenticationForm (django.contrib.auth.forms)
    template_name = 'auth/login.html' # Default: registration/login.html
    login_url = '/auth/login/' # Defaults to LOGIN_URL
    next_page = '/auth/profile/' # Defaults to LOGIN_REDIRECT_URL
    redirect_authenticated_user = True # If it is false, authenticated_user is still access to login


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/auth/login/' # if not default render to template
    # template_name = 'auth/logged_out.html' # Default: registration/logged_out.html


class PasswordChange(PasswordChangeView):
    template_name = 'auth/password_change_form.html' # Default: registration/password_change_form.html
    success_url = reverse_lazy('password_change_done')
    title = _('Password change')


class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html' # Default: registration/password_change_done.html
    title = _('Password change successful')


class PasswordReset(PasswordResetView):
    template_name = 'auth/password_reset_form.html' # Default: registration/password_reset_form.html
    success_url = reverse_lazy('password_reset_done')
    title = _('Password reset')
    from_email = 'system@sys.com'
    email_template_name = 'auth/password_reset_email.html' # Default: registration/password_reset_email.html
    subject_template_name = 'auth/password_reset_subject.txt' # Default: registration/password_reset_subject.txt


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html' # Default: registration/password_reset_done.html
    title = _('Password reset sent')


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html' # Default: registration/password_reset_confirm.html
    title = _('Enter new password')
    success_url = reverse_lazy('password_reset_complete')

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html' # Default: registration/password_reset_complete.html
    title = _('Password reset complete')


class Register(FormView):
    template_name = 'register.html'
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
    template_name = 'register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')
        return context

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'
