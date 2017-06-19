from rest_framework import serializers

from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='accounts_detail'
    )

    class Meta:
        model = Account
        fields = ('id', 'iban', 'balance',)
