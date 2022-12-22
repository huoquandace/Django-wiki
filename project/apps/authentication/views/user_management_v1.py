from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin


class Index(TemplateView):
    template_name = 'index.html'


from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()
from csv import reader
def userdata(request):
    try:
        with open('templates/csv.csv', 'r') as csv_file:
            csvf = reader(csv_file)
            data = []
            for id, username, password, *__ in csvf:
                user = User(username=username)
                user.set_password(password)
                data.append(user)
            User.objects.bulk_create(data)
        csv_file.close()
    except Exception as e:
        print(e)
    return JsonResponse('user csv is now working', safe=False)


class ImportUser(LoginRequiredMixin, View):
    pass