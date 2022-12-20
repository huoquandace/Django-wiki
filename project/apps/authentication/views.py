from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView

from authentication.forms import RegisterForm, AuthForm


class Login(LoginView):
    authentication_form = AuthForm
    template_name = 'login.html'
    login_url = '/auth/login/' # Defaults to LOGIN_URL
    next_page = '/auth/profile/' # Defaults to LOGIN_REDIRECT_URL
    redirect_authenticated_user = True # If it is false, authenticated_user is still access to login

class Register(FormView):
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):
        data = form.cleaned_data
        from pprint import pprint; pprint(data) # DEBUG
        new_user = get_user_model().objects.create_user(
            username = data['username'],
            password = data['password1'],
            email = data['email'],
        )
        url = f"{reverse('register_done')}?username={new_user.username}"
        from pprint import pprint; pprint(url) # DEBUG
        return redirect(url)

class RegisterDone(TemplateView):
    template_name = 'register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')
        return context

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/auth/login/' # if not default render to template
    # template_name = 'logout.html'