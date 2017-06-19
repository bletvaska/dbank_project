from django.contrib import admin

# Register your models here.
from django.urls import reverse

from .models import Client, Account, Transaction


class AdminAccout(admin.ModelAdmin):
    list_display = ('iban', 'created', 'balance', 'get_owner_name', 'is_open', 'nr_of_transactions')
    ordering = ('-created',)
    search_fields = ('iban', 'owner__name')
    # list_filter = ('owner',)
    # exclude = ('closed', 'balance',)

    def get_owner_name(self, obj):
        ct = obj.owner._meta  # content type
        url = reverse('admin:{}_{}_change'.format(ct.app_label, ct.model_name), args=(obj.owner.pk,))
        return '<a href="{}">{}</a>'.format(url, obj.owner.name)

    get_owner_name.short_description = 'owner'
    get_owner_name.allow_tags = True

    def nr_of_transactions(self, obj):
        transactions = Transaction.objects.extra(
            where=["src_id={0} OR dest_id={0}".format(obj.pk)]).values_list('id', flat=True)
        if transactions.count() == 0:
            return '0'
        return '<a href="/admin/account/transaction/?pk__in={}">{}</a>'.format(str(list(transactions))[1:-1],
                                                                               transactions.count())

    nr_of_transactions.short_description = 'Transactions'
    nr_of_transactions.allow_tags = True


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


class AdminClient(admin.ModelAdmin):
    list_display = ('get_full_name', 'list_accounts')

    def list_accounts(self, obj):
        accounts = obj.account_set.count()
        if accounts == 0:
            return '0'

        return '<a href="/admin/account/account/?owner__id__exact={}">{}</a>'.format(
            obj.id, accounts)

    list_accounts.short_description = 'Accounts'
    list_accounts.allow_tags = True


admin.site.register(Account, AdminAccout)
admin.site.register(Transaction, AdminTransaction)
admin.site.register(Client, AdminClient)
