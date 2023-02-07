###### Setting

# Generating a SECRET_KEY using the terminal
py manage.py shell
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

# Turn off warning messages
SILENCED_SYSTEM_CHECKS = ["admin.W411"]

# Create app in subdir
mkdir apps/app_name
startapp polls apps/app_name

# Change Project root
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# VsCode
```
// Turn off missing module report
"python.analysis.diagnosticSeverityOverrides": {
    "reportMissingModuleSource": "none"
}
```

# Lang

```
django-admin makemessages --all --ignore=env
django-admin compilemessages --ignore=env
```
