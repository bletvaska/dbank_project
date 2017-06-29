from django.forms import ModelForm

from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['src', 'dest', 'amount']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['src'] = kwargs['initial']['src']
        self.fields['dest'] = kwargs['initial']['dest']