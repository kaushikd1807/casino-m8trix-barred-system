from django.contrib import admin
from django.utils.html import format_html

from .models import Order, Document


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('qr_code',)

    def qr_code(self, obj):
        return format_html('<img src="{}" />'.format(obj.qr_code))


admin.site.register(Order, OrderAdmin)
admin.site.register(Document)
