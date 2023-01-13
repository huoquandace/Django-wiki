import os
from csv import reader

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import (
    View,
    TemplateView, FormView,
    ListView, UpdateView, DetailView
)

from common.forms import UploadFileForm
from common.utils import html_to_pdf
from authentication.models.base import User
from authentication.models.extra import Profile
from authentication.forms.extra import ProfileUpdateForm, UserAddForm, UserProfileForm


CSV_FILE_PATH = 'data/csv/'
USER_CSV_FILE_TEMPLALTE = 'data/csv.csv'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'extra/profile.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'extra/profile_update.html'
    context_object_name = 'user'
    queryset = Profile.objects.all()
    form_class = ProfileUpdateForm

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        user = self.request.user
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user.profile, initial={'email': user.email})
        return context

    def form_valid(self, form):
        profile = form.save(commit=False) # commit=false => Create model object to add extra data before save it
        user = profile.user
        user.email = form.cleaned_data['email']
        user.save()
        profile.save()
        return redirect('profile')
        # return HttpResponseRedirect(reverse('profile:user-profile', kwargs={'pk': self.get_object().id}))

class ProfileUpdateView2(LoginRequiredMixin, View):
    
    from django import forms
    class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = '__all__'

    class UserForm(forms.ModelForm):
        class Meta:
            model = User
            # fields = '__all__'
            fields = ('username', 'email')

    def get(self, request):
        profile_form = self.ProfileForm(instance=request.user.profile)
        user_form = self.UserForm(instance=request.user)
        context = {
            'profile_form': profile_form,
            'user_form': user_form,
        }
        return render(request, 'extra/profile_update2.html', context)
    
    def post(self, request):
        profile_form = self.ProfileForm(request.POST, request.FILE)
        user_form = self.UserForm(request.POST)


class UserAdd(LoginRequiredMixin, View):
    
    def get(self, request):
        form = UserProfileForm()
        acc_form = UserAddForm()
        context = {
            'form': form,
            'acc_form': acc_form,
        }
        return render(request, 'extra/user_add.html', context)
    
    def post(self, request):
        form = UserProfileForm(request.POST)
        acc_form = UserAddForm(request.POST)
        try:
            if request.POST['custom_acc'] and acc_form.is_valid():
                user = User(username=acc_form.cleaned_data['username'])
                user.set_password(acc_form.cleaned_data['password'])
                user.save(commit=False)
                print(user)
            else:
                messages.error(request, acc_form.errors)
        except MultiValueDictKeyError:
            acc_form = UserAddForm()
            if form.is_valid():
                u_id = form.cleaned_data['u_id']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                username = last_name
                fn_arr = first_name.strip().split(' ')
                for c in fn_arr:
                    username += c[0].upper()
                username += str(u_id)
                birthday = form.cleaned_data['birthday']
                password = str(birthday).replace('-', '')
                user = User(username=username)
                user.set_password(password)
                user.save()
                return redirect('user_add')
            else:
                return redirect('user_add')
        except Exception as e:
            print(e)
        context = {
            'form': form,
            'acc_form': acc_form,
        }
        return render(request, 'extra/user_add.html', context)
    

class UserDetail(DetailView):
    model = User
    template_name = 'extra/user_detail.html'
    context_object_name = 'user'

class UserList(ListView):
    template_name = 'extra/user_list.html'
    model = User
    context_object_name = 'objects'

class UserListToPdf(View):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        open('templates/reports/temp.html', "w").write(render_to_string('reports/staff.html', {'users': users}))
        pdf = html_to_pdf('reports/temp.html')
        return HttpResponse(pdf, content_type='application/pdf')

class UserAddCsv(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'extra/user_add_csv.html'

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



