from django.db import models
from django.core.exceptions import ValidationError


def validate_amount(value):
    if value < 0:
        raise ValidationError('Amount must be positive number.')


# def validate_closed_account(account):
#     if account.is_closed():
#         raise ValidationError("Account can't be closed.")


# Create your models here.
class Transaction(models.Model):
    timestamp = models.DateTimeField('transaction timestamp', auto_now_add=True)
    src = models.ForeignKey('accounts.Account', default=None, null=True)
    dest = models.ForeignKey('accounts.Account', default=None, related_name='target', null=True)
    amount = models.FloatField('transaction amount', null=False, validators=[validate_amount])

    @property
    def type(self):
        if self.src is None:
            return 'deposit'
        elif self.dest is None:
            return 'withdraw'
        else:
            return 'transaction'

    def __str__(self):
        if self.src is None:
            return f'deposit to {self.dest} at {self.timestamp}: {self.amount}'
        elif self.dest is None:
            return f'withdraw from {self.src} at {self.timestamp}: {self.amount}'
        else:
            return f'transaction from {self.src} to {self.dest} at {self.timestamp}: {self.amount}'

    def proceed(self):
        # TODO testnut, ci zbehne kontrola na zatvoreny/otvoreny ucet
        if self.timestamp is not None:
            raise ValueError(f'Transaction already proceeded at {self.timestamp}')

        self.src.balance -= self.amount
        self.src.save()
        self.dest.balance += self.amount
        self.dest.save()

        # save
        self.save()
