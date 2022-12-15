from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, Brokerage, Country
from django.contrib.auth.models import Group


# Register your models here.

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': (
            'phone',
            'address1',
            'address2',
            'city',
            'zip_code',
            'country',
            'brokerage',
            'profile_photo',
            'user_type',
        )}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': (
            'phone',
            'address1',
            'address2',
            'city',
            'zip_code',
            'country',
            'brokerage',
            'profile_photo',
            'user_type',
        )}),
    )

    readonly_fields = UserAdmin.readonly_fields + (
        'uuid',
        'created_at',
        'updated_at'
    )

    pass


admin.site.register(User, CustomUserAdmin)
admin.site.register(Brokerage)
admin.site.register(Country)
admin.site.unregister(Group)
