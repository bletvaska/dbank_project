from django.forms import ModelForm

from account.models import Account, Transaction


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['iban']

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        self.owner = owner
        super(AccountForm, self).__init__(*args, **kwargs)


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['src', 'dest', 'amount']


