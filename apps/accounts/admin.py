from django.contrib import admin
from apps.accounts.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'user_type',
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (
            'user_type',
        )}),
    )


admin.site.register(User, CustomUserAdmin)


# class UserAdmin(admin.ModelAdmin):
#     list_display = ("id", "first_name", "username", "user_type")
#
#
# admin.site.register(User, UserAdmin)
