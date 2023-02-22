
from django.urls import reverse_lazy
from django.core import exceptions
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class Login(LoginView):

    class AuthForm(AuthenticationForm):
        error_messages = {
            'invalid_login': _("Please enter a correct %(username)s and password. Note that both fields may be case-sensitive."),
            'inactive': _("UR CUSTOM MESSAGE"),
        }

        def confirm_login_allowed(self, user):
            # return
            if not user.is_active:
                raise exceptions.ValidationError(_("This account is inactive."), code='inactive',)
            if user.username.startswith('b'):
                raise exceptions.ValidationError(_("Sorry, accounts starting with 'b' aren't welcome here."), code='no_b_users',)
            
    accounts_form = AuthForm
    template_name = 'auth/login.html'
    login_url = reverse_lazy('login')
    next_page = reverse_lazy('auth_index')
    redirect_authenticated_user = True # If it is false, authenticated_user is still access to login


class Logout(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

