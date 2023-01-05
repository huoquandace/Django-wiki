import os
from csv import reader

from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView, View, ListView
from django.core.files.storage import FileSystemStorage

from common.forms import UploadFileForm
from authentication.models import User


CSV_FILE_PATH = 'data/csv/'
USER_CSV_FILE_TEMPLALTE = 'data/csv.csv'


class UserList(ListView):
    template_name = 'index1.html'
    model = User
    context_object_name = 'objects'

class ImportUser(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'ver_1/import.html'

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



