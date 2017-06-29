from django.contrib import admin

# Register your models here.
from django.urls import reverse

from transactions.models import Transaction
from .models import Account


@admin.register(Account)
class AdminAccout(admin.ModelAdmin):
    list_display = ('iban', 'created', 'balance', 'get_owner_name', 'is_open', 'nr_of_transactions')
    ordering = ('-created',)
    search_fields = ('iban', 'owner__name')
    # list_filter = ('owner',)
    # exclude = ('closed', 'balance',)

    def get_owner_name(self, obj):
        ct = obj.owner._meta  # content type
        url = reverse('admin:{}_{}_change'.format(ct.app_label, ct.model_name), args=(obj.owner.pk,))
        return '<a href="{}">{}</a>'.format(url, obj.owner.get_full_name())

    get_owner_name.short_description = 'owner'
    get_owner_name.allow_tags = True

    def nr_of_transactions(self, obj):
        transactions = Transaction.objects.extra(
            where=["src_id={0} OR dest_id={0}".format(obj.pk)]).values_list('id', flat=True)
        if transactions.count() == 0:
            return '0'
        return '<a href="/admin/accounts/transaction/?pk__in={}">{}</a>'.format(str(list(transactions))[1:-1],
                                                                               transactions.count())

    nr_of_transactions.short_description = 'Transactions'
    nr_of_transactions.allow_tags = True

# admin.site.register(Account, AdminAccout)


