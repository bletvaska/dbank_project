from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Client(AbstractUser):
    name = models.CharField('clients name', max_length=128, null=False)
    phone_number = models.CharField('phone number', max_length=64, null=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class Account(models.Model):
    iban = models.CharField('iban', max_length=10, null=False, unique=True)
    created = models.DateTimeField('creation date', auto_now_add=True)
    closed = models.DateTimeField('closed date', default=None, null=True, blank=True)
    balance = models.FloatField('current balance', default=0, null=False, blank=True)
    owner = models.ForeignKey(Client, null=False)

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

        self.amount -= amount
        self.save()
        dest.amount += amount
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

    def __str__(self):
        return '{} ({}) {}'.format(self.iban, self.owner.name, self.balance)

    # def get_absolute_url(self):
    #     # from django.urls import reverse
    #     return reverse('account.views.details', args=[str(self.id)])


class Transaction(models.Model):
    timestamp = models.DateTimeField('transaction timestamp', auto_now_add=True)
    src = models.ForeignKey('Account', default=None, null=True)
    dest = models.ForeignKey('Account', default=None, related_name='target', null=True)
    amount = models.FloatField('transaction amount', null=False)

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
