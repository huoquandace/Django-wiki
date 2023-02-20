Intro: https://django.fun/en/docs/django/4.1/intro/
General:
    Models:
        - Definition syntax 
            [field_name] = models.ForeignKey('[app_label].[model_name]', on_delete=models.CASCADE)
    Admin:
        - Register all of models in app
            from django.apps import apps
            from django.contrib import admin
            for model in apps.get_app_config('polls').get_models():
                try: admin.site.register(model)
                except admin.sites.AlreadyRegistered: pass
    Templates:
        - Format date:
            {{ [date_value]|date:'[date_format]]' }}
        - Get all foreign objects
            Object.[field]_set.all / Objdect.[related_name].all
        - For loop (Built-in):
            forloop.counter / forloop.counter0 / forloop.revcounter / forloop.revcounter0 / forloop.first / forloop.last / forloop.parentloop
        - Fieldset, Legend
    Response:
        - Response string
            django.http -> HttpResponse('[content]')
        - Render template
            django.http -> HttpResponse( ','.join([object.[field] for object in [objects]]) )
            django.http -> HttpResponse( django.template->loader.get_template('[template_path]').render([context], request) )
            django.shortcut -> render(request, '[template_path]', [context])
        - 404:
            django.shortcut->get_object_or_404 = raise: django.http->Http404 + Object.objects.get()
            django.shortcut->get_list_or_404 = raise: django.http->Http404 + Object.objects.filter()
    Database:
        - Settings
            'ENGINE': 'django.db.backends.[sqlite3/postgresql/mysql/oracle]',
            'NAME': '[dbname/db.sqlite3_path]',
            'USER': '[username]',
            'PASSWORD': '[password]',
            'HOST': '[hostname]',
            'PORT': '[port_number]',
        - Export sql from migrations
            python manage.py sqlmigrate polls [migration_number]
    Time:
        - Pub two datetime:
            ex: timezone.now() - datetime.timedelta(days=1)
    Shell:
        - Search:
            object_name].objects.get([field_name]__startswith='[search_word]')
            object_name].objects.get([field_name]__contains='[search_word]')
            object_name].objects.get([field_name]__year='[search_datetime_year]')
    Url:
        - Removing hardcoded URLs
            - Set name for path
        - Namespacing URL: 
            app_name = '[app_name]'
    Exceptions:
        - KeyError: if field is not provided in POST