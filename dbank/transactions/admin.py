from django.contrib import admin

# Register your models here.
from django.urls import reverse

from .models import Transaction

@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = ('get_type', 'timestamp', 'get_src', 'get_dest', 'amount')
    ordering = ('-timestamp',)
    list_display_links = None

    def get_type(self, obj):
        if obj.src is None:
            return 'deposit'
        elif obj.dest is None:
            return 'withdraw'
        else:
            return 'transaction'

    get_type.short_description = 'Type'

    def get_src(self, obj):
        if obj.src is None:
            return None
        ct = obj.src._meta  # content type
        url = reverse('admin:{}_{}_change'.format(ct.app_label, ct.model_name), args=(obj.src.pk,))
        return '<a href="{}">{}</a>'.format(url, obj.src.iban)

    get_src.short_description = 'Source'
    get_src.allow_tags = True

    def get_dest(self, obj):
        if obj.dest is None:
            return None
        ct = obj.dest._meta  # content type
        url = reverse('admin:{}_{}_change'.format(ct.app_label, ct.model_name), args=(obj.dest.pk,))
        return '<a href="{}">{}</a>'.format(url, obj.dest.iban)

    get_dest.short_description = 'Destination'
    get_dest.allow_tags = True

# admin.site.register(Transaction, AdminTransaction)