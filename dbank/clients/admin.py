from django.contrib import admin

# Register your models here.
from django.urls import reverse

from .models import Client


@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ('get_full_name', 'list_accounts')

    def list_accounts(self, obj):
        accounts = obj.account_set.count()
        if accounts == 0:
            return '0'

        url = '{}?owner__id__exact={}'.format(reverse('admin:accounts_account_changelist'), obj.id)
        return '<a href="{}">{}</a>'.format(url, accounts)

    list_accounts.short_description = 'Accounts'
    list_accounts.allow_tags = True

    Client.get_full_name.short_description = 'Full Name'
