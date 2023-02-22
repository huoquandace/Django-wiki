"""
    To do: permission provider, reset password user account,
"""


import os
from csv import reader
from django import forms
from django.conf import settings
from django.urls import reverse_lazy, reverse, URLPattern, URLResolver
from django.core import exceptions
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import *
from django.contrib.auth.mixins import *
from django.contrib.auth.forms import *
from django.contrib.auth.models import Group
from django.views.generic import *
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

from accounts.models.profile_model import Profile
from accounts.forms.base import UploadFileForm
from accounts.utils.base import html_to_pdf
from common.mixins import *

CSV_FILE_PATH = 'data/csv/'
USER_CSV_FILE_TEMPLALTE = 'data/csv.csv'


class AuthIndex(StaffRequiredMixin, TemplateView):
    template_name = 'auth_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        urlconf = __import__('apps.accounts.urls', {}, {}, [''])
        def list_urls(lis, acc=None):
            acc = [] if acc is None else acc
            if not lis: return None
            l = lis[0]
            if isinstance(l, URLPattern):
                yield acc + [str(l.pattern)]
            elif isinstance(l, URLResolver):
                yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
            yield from list_urls(lis[1:], acc)
        url_list = []
        for p in list_urls(urlconf.urlpatterns, ['']):
            url_list.append(''.join(p)) 
        context['url_list'] = url_list

        return context


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


class UserDetail(DetailView):
    model = get_user_model()
    template_name = 'auth/user_detail.html'
    context_object_name = 'user'


class UserList(ListView):
    template_name = 'auth/user_list.html'
    model = get_user_model()
    context_object_name = 'users'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return self.model.objects.filter(username__icontains=query)
        return super().get_queryset()


class UserAdd(CreateView):
    model = get_user_model()
    fields = ['username', 'password']
    template_name = 'auth/user_add.html'

    def form_valid(self, form):
        user = form.save()
        user.set_password(user.password)
        user.save()
        return redirect('user_list')


class UserEdit(LoginRequiredMixin, View):
    
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['gender', 'phone', 'age', 'birthday', 'avatar' ,'address',]

    class UserForm(forms.ModelForm):
        username = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
        class Meta:
            model = get_user_model()
            fields = ('username', 'email', 'first_name', 'last_name')

    def get(self, request, pk):
        user = get_user_model().objects.get(id=pk)
        profile_form = self.ProfileForm(instance=user.profile)
        user_form = self.UserForm(instance=user)
        context = {
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'auth/user_edit.html', context)
    
    def post(self, request, pk):
        user = get_user_model().objects.get(id=pk)
        user_form = self.UserForm(request.POST, instance=user)
        profile_form = self.ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Edit successfully')
            return redirect('user_edit', pk=user.id)
        else:
            messages.error(request, 'errors')
            return redirect('user_edit')


class UserDelete(DeleteView):
    model = get_user_model()
    template_name = 'auth/user_delete.html'
    success_url = reverse_lazy('user_list')


class UserAddByInfo(LoginRequiredMixin, View):
    
    class UserProfileForm(forms.ModelForm):
        first_name = forms.CharField(max_length=100, required = False)
        last_name = forms.CharField(max_length=100, required = False)
        
        class Meta:
            model = Profile
            fields = ['first_name', 'last_name', 'gender', 'phone', 'age', 'birthday', 'avatar' ,'address',]

    class UserAddForm(forms.Form):
        username = forms.CharField(max_length=100, required = False)
        password = forms.CharField(max_length=100, required = False)
        
        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                get_user_model().objects.get(username=username)
            except get_user_model().DoesNotExist:
                return username
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    def get(self, request):
        return render(request, 'auth/user_add_by_info.html', {
            'form': self.UserProfileForm(),
            'acc_form': self.UserAddForm(),
        })
    
    def post(self, request):
        def isBlank(s): return not(s and s.strip())
        def isNotBlank(s): return s and s.strip()

        form = self.UserProfileForm(request.POST)
        acc_form = self.UserAddForm(request.POST)
        if request.POST.get('custom_acc', 0) != 0:
            if acc_form.is_valid():
                user = get_user_model()(username=acc_form.cleaned_data['username'])
                user.set_password(acc_form.cleaned_data['password'])
                user.save()
                return redirect('user_list')
            else:
                messages.error(request, acc_form.errors)
        else:
            acc_form = self.UserAddForm()
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                if isBlank(first_name) or isBlank(last_name):
                    messages.error(request, "name is neccesary for create account")
                    return redirect('user_add_by_info')
                username = last_name
                fn_arr = first_name.strip().split(' ')
                for c in fn_arr: username += c[0]
                user = get_user_model()(username=username)
                user.set_password("123")
                user.save()
                return redirect('user_list')
            else:
                messages.error(request, form.errors)
                return redirect('user_add_by_info')
        return render(request, 'auth/user_add_by_info.html', {
            'form': form,
            'acc_form': acc_form,
        })


class UserAddByCsv(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'auth/user_add_by_csv.html'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        fs = FileSystemStorage(location=CSV_FILE_PATH)
        filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename) # If not set location in fs, Default to MEDIA_ROOT
        file_path = os.path.join(CSV_FILE_PATH, filename)
        try:
            with open(file_path, 'r') as csv_file:
                csvf = reader(csv_file)
                User = get_user_model()
                data = []
                for id, username, password, *__ in csvf:
                    user = User(username=username)
                    user.set_password(password)
                    data.append(user)
                User.objects.bulk_create(data)
            csv_file.close()
        except Exception as e:
            messages.error(self.request, e)
            return HttpResponseRedirect(self.request.path_info)
        return JsonResponse('Successful', safe=False)


class DowloadUserCsvTemplate(View):

    def get(self, request, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, USER_CSV_FILE_TEMPLALTE)
        try:
            # check os.path.exists(file_path)
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        except Exception as e:
            print(e)
        return HttpResponseRedirect(request.path_info)


class UserListToPdf(View):
    
    def get(self, request, *args, **kwargs):
        import accounts, os
        app_dir = os.path.dirname(accounts.__file__)
        temp_dir = os.path.join(app_dir, "templates/reports/temp.html")
        users = get_user_model().objects.all()
        open(temp_dir, "w").write(render_to_string('reports/staff.html', {'users': users}))
        pdf = html_to_pdf(temp_dir)
        return HttpResponse(pdf, content_type='application/pdf')


class UserGroupList(ListView):
    template_name = 'auth/user_group_list.html'
    model = Group
    context_object_name = 'groups'


class UserGroupAdd(CreateView):
    model = Group
    fields = '__all__'
    template_name = 'auth/user_group_add.html'





