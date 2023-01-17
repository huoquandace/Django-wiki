"""
    Defaut django.auth: registration/
    Custom to: auth/
"""

from django import urls
from django.shortcuts import redirect
from django.contrib import auth
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.core import exceptions
from django import forms


class AuthIndex(generic.TemplateView):
    template_name = 'auth_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        urlconf = __import__('apps.authentication.routes.base', {}, {}, [''])
        def list_urls(lis, acc=None):
            acc = [] if acc is None else acc
            if not lis: return None
            l = lis[0]
            if isinstance(l, urls.URLPattern):
                yield acc + [str(l.pattern)]
            elif isinstance(l, urls.URLResolver):
                yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
            yield from list_urls(lis[1:], acc)
        url_list = []
        for p in list_urls(urlconf.urlpatterns, ['']):
            url_list.append(''.join(p)) 
        context['url_list'] = url_list

        return context


class Login(auth.views.LoginView):

    class AuthForm(auth.forms.AuthenticationForm):
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
            
    authentication_form = AuthForm
    template_name = 'auth/login.html'
    login_url = '/auth/login/'
    next_page = '/auth/extra/profile/'
    redirect_authenticated_user = True # If it is false, authenticated_user is still access to login


class Logout(auth.mixins.LoginRequiredMixin, auth.views.LogoutView):
    next_page = '/auth/login/' # if not default render to template
    # template_name = 'auth/logged_out.html'


class PasswordChange(auth.mixins.LoginRequiredMixin, auth.views.PasswordChangeView):
    template_name = 'auth/password_change_form.html'
    success_url = urls.reverse_lazy('password_change_done')


class PasswordChangeDone(auth.mixins.LoginRequiredMixin, auth.views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'


class PasswordReset(auth.views.PasswordResetView):
    template_name = 'auth/password_reset_form.html'
    success_url = urls.reverse_lazy('password_reset_done')
    from_email = 'system@sys.com'
    email_template_name = 'auth/password_reset_email.html'
    subject_template_name = 'auth/password_reset_subject.txt'


class PasswordResetDone(auth.views.PasswordResetDoneView):
    template_name = 'auth/password_reset_done.html'


class PasswordResetConfirm(auth.views.PasswordResetConfirmView):
    template_name = 'auth/password_reset_confirm.html'
    success_url = urls.reverse_lazy('password_reset_complete')

class PasswordResetComplete(auth.views.PasswordResetCompleteView):
    template_name = 'auth/password_reset_complete.html'


class Register(generic.FormView):

    class RegisterForm(auth.forms.UserCreationForm):
        class Meta:
            model = auth.get_user_model()
            fields = ('username', 'email')
            field_classes = {'username': auth.forms.UsernameField}
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
        new_user = auth.get_user_model().objects.create_user(
            username = data['username'],
            password = data['password1'],
            email = data['email'],
        )
        url = f"{urls.reverse('register_done')}?username={new_user.username}"
        return redirect(url)

class RegisterDone(generic.TemplateView):
    template_name = 'auth/register_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.GET.get('username')
        return context
