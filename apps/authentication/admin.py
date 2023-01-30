from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from authentication.models.base import User, Profile


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            # 'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'user_permissions', 'groups', )
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'is_staff', 'groups')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user_permissions', 'is_active', 'is_superuser', )
        }),
    )
    list_display = ('username', 'email', 'date_joined')
    list_filter = ('is_staff', 'is_active', )
    search_fields = ('last_name__startswith', )

    class Meta:
        ordering = ('date_joined', )


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
# admin.site.unregister(Group)
