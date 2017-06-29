from django.db import models
from rest_framework.exceptions import ValidationError


def validate_amount(value):
    if value < 0:
        raise ValidationError('Amount must be positive number.')


# Create your models here.
class Transaction(models.Model):
    timestamp = models.DateTimeField('transaction timestamp', auto_now_add=True)
    src = models.ForeignKey('accounts.Account', default=None, null=True)
    dest = models.ForeignKey('accounts.Account', default=None, related_name='target', null=True)
    amount = models.FloatField('transaction amount', null=False, validators=[validate_amount])

    def get_type(self):
        if self.src is None:
            return 'deposit'
        elif self.dest is None:
            return 'withdraw'
        else:
            return 'transaction'

    def __str__(self):
        if self.src is None:
            return 'deposit to {} at {}: {}'.format(self.dest, self.timestamp, self.amount)
        elif self.dest is None:
            return 'withdraw from {} at {}: {}'.format(self.src, self.timestamp, self.amount)
        else:
            return 'transaction from {} to {} at {}: {}'.format(self.src, self.dest, self.timestamp, self.amount)
