import datetime

import re
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
from django.urls import reverse
from transactions.models import Transaction


def validate_iban(value):
    match = re.search('^[A-Z]{2}\d+$', value)
    if not match:
        raise ValidationError('IBAN has wrong format.')


def validate_amount(value):
    if value < 0:
        raise ValidationError('Amount must be positive number.')


class Account(models.Model):
    iban = models.CharField('iban', max_length=10, null=False, unique=True, validators=[validate_iban])
    created = models.DateTimeField('creation date', auto_now_add=True)
    closed = models.DateTimeField('closed date', default=None, null=True, blank=True)
    balance = models.FloatField('current balance', default=0, null=False, blank=True)
    owner = models.ForeignKey('clients.Client', null=False)
    overdraft = models.FloatField('allowed overdraft', default=0, null=False)

    def deposit(self, amount):
        if self.is_closed():
            raise ValueError('Account is closed')

        self.balance += amount
        self.save()

        # make transaction
        Transaction(dest=self, amount=amount).save()

    def withdraw(self, amount):
        if self.is_closed():
            raise ValueError('Account is closed')

        self.balance -= amount
        self.save()

        # make transaction
        Transaction(src=self, amount=amount).save()

    def transfer(self, dest, amount):
        # check if accounts are open first
        if self.is_closed():
            raise ValueError('Source Account is Closed')

        if dest.is_closed():
            raise ValueError('Destination Account is Closed')

        self.balance -= amount
        self.save()
        dest.balance += amount
        dest.save()

        # make transaction
        Transaction(src=self, dest=dest, amount=amount).save()

    def is_open(self):
        return self.closed is None
    is_open.boolean = True

    def is_closed(self):
        return not self.is_open()

    def transactions(self):
        return self.transaction_set.all() | self.target.all()

    def close(self, close_date=None):
        if self.closed is not None:
            raise Exception('Account is already closed.')
        if self.balance != 0:
            raise Exception('Account is not empty.')
        if close_date is None:
            self.closed = datetime.datetime.now()
        else:
            self.closed = close_date
        self.save()

    def __str__(self):
        return '{} ({})'.format(self.iban, self.owner.get_full_name())

    # def get_absolute_url(self):
    #     return reverse('accounts.views.details', args=[str(self.id)])
