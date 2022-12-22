from csv import reader

from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from common.forms import UploadFileForm


CSV_FILE_PATH = 'data/csv'

class Index(TemplateView):
    template_name = 'index.html'


class ImportUser(LoginRequiredMixin, FormView):
    form_class = UploadFileForm
    template_name = 'user_management_v1/import.html'

    def form_valid(self, form):
        file = form.cleaned_data['file']
        fs = FileSystemStorage(location=CSV_FILE_PATH)
        filename = fs.save(file.name, file)
        # uploaded_file_url = fs.url(filename) # If not set location in fs, Default to MEDIA_ROOT
        file_path = CSV_FILE_PATH + '/' + filename
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
            print(e)
        return JsonResponse('Successful', safe=False)
