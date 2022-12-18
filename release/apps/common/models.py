from django.db import models


class BaseModel(models.Model):
    # created_at = models.DateTimeField(False, True, editable=False)
    # updated_at = models.DateTimeField(True, True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True