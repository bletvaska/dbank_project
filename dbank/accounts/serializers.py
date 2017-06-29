from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ('url', 'iban', 'owner', 'balance', 'closed')

