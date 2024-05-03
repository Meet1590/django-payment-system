from django.contrib import admin

# Register your models here.
from .models import CustomUser

from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(CustomUser, CustomUserAdmin)
