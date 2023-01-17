import os, re
from csv import reader

from django.template.defaultfilters import slugify
from django import forms
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import *
from django.urls import URLPattern, URLResolver
from django.utils.translation import gettext_lazy as _

# from common.forms import UploadFileForm
# from common.utils import html_to_pdf
from authentication.models.base import Profile
# from authentication.forms.extra import ProfileUpdateForm, UserAddForm, UserProfileForm


CSV_FILE_PATH = 'data/csv/'
USER_CSV_FILE_TEMPLALTE = 'data/csv.csv'


class AuthExtra(TemplateView):
    template_name = 'auth_extra.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        urlconf = __import__('apps.authentication.routes.extra', {}, {}, [''])
        def list_urls(lis, acc=None):
            if acc is None:
                acc = []
            if not lis:
                return
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


class UserDetail(DetailView):
    model = get_user_model()
    template_name = 'extra/user_detail.html'
    context_object_name = 'user'


class UserAdd(View):

    class UserProfileForm(forms.Form):
        first_name = forms.CharField(max_length=100, required = False)
        last_name = forms.CharField(max_length=100, required = False)
        birthday = forms.CharField(max_length=100, required = False)

    class UserAddForm(forms.Form):
        username = forms.CharField(max_length=100, required = False)
        password = forms.CharField(max_length=100, required = False)
        
        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                user = get_user_model().objects.get(username=username)
            except user.DoesNotExist:
                return username
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)

    def get(self, request):
        form = self.UserProfileForm()
        acc_form = self.UserAddForm()
        context = {
            'form': form,
            'acc_form': acc_form,
        }
        
        # string = slugify(u"những-viên-kẹo")
        # string = re.sub('[^A-Za-z0-9]+', '', string)

        return render(request, 'extra/user_add.html', context)
    
    def post(self, request):
        form = self.UserProfileForm(request.POST)
        acc_form = self.UserAddForm(request.POST)
        result = request.POST.get('custom_acc', 0)
        print(result)
        # try:
        #     if request.POST['custom_acc'] and acc_form.is_valid():
        #         user = get_user_model()(username=acc_form.cleaned_data['username'])
        #         user.set_password(acc_form.cleaned_data['password'])
        #         # user.save(commit=False)
        #         print('ok')
        #     else:
        #         messages.error(request, acc_form.errors)
        # except MultiValueDictKeyError:
        #     acc_form = self.UserAddForm()
        #     if form.is_valid():
        #         first_name = acc_form.cleaned_data['first_name']
        #         last_name = acc_form.cleaned_data['last_name']
        #         username = last_name
        #         fn_arr = first_name.strip().split(' ')
        #         for c in fn_arr:
        #             username += c[0].upper()
        #         birthday = form.cleaned_data['birthday']
        #         password = str(birthday).replace('-', '')
        #         password = str(birthday).replace('/', '')
        #         user = get_user_model()(username=username)
        #         user.set_password(password)
        #         # user.save()
        #         return redirect('/auth/extra/user/' + str(user.id))
        #     else:
        #         messages.error(request, form.errors)
        #         return redirect('user_add')
        # except Exception as e:
        #     print(e)
        context = {
            'form': form,
            'acc_form': acc_form,
        }
        return render(request, 'extra/user_add.html', context)


class UserList(ListView):
    template_name = 'extra/user_list.html'
    model = get_user_model()
    context_object_name = 'users'


class UserDelete(SuccessMessageMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('user_list')
    template_name = 'extra/user_delete.html'
    success_message = _("User was deleted successfully.")



# class UserListToPdf(View):
#     def get(self, request, *args, **kwargs):
#         users = User.objects.all()
#         open('templates/reports/temp.html', "w").write(render_to_string('reports/staff.html', {'users': users}))
#         pdf = html_to_pdf('reports/temp.html')
#         return HttpResponse(pdf, content_type='application/pdf')

# class UserAddCsv(LoginRequiredMixin, FormView):
#     form_class = UploadFileForm
#     template_name = 'extra/user_add_csv.html'

#     def form_valid(self, form):
#         file = form.cleaned_data['file']
#         fs = FileSystemStorage(location=CSV_FILE_PATH)
#         filename = fs.save(file.name, file)
#         # uploaded_file_url = fs.url(filename) # If not set location in fs, Default to MEDIA_ROOT
#         file_path = os.path.join(CSV_FILE_PATH, filename)
#         try:
#             with open(file_path, 'r') as csv_file:
#                 csvf = reader(csv_file)
#                 User = get_user_model()
#                 data = []
#                 for id, username, password, *__ in csvf:
#                     user = User(username=username)
#                     user.set_password(password)
#                     data.append(user)
#                 User.objects.bulk_create(data)
#             csv_file.close()
#         except Exception as e:
#             messages.error(self.request, e)
#             return HttpResponseRedirect(self.request.path_info)
#         return JsonResponse('Successful', safe=False)


# class DowloadUserCsvTemplate(View):

#     def get(self, request, *args, **kwargs):
#         file_path = os.path.join(settings.BASE_DIR, USER_CSV_FILE_TEMPLALTE)
#         try:
#             # check os.path.exists(file_path)
#             with open(file_path, 'rb') as fh:
#                 response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#                 response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#                 return response
#         except Exception as e:
#             print(e)
#         return HttpResponseRedirect(request.path_info)


