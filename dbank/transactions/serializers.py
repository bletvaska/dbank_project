from rest_framework import serializers

from accounts.models import Account
from .models import Transaction


def validate_account(iban):
    account = Account.objects.filter(iban=iban).first()

    if account is None:
        raise serializers.ValidationError("Account doesn't exist.")

    if account.is_closed():
        raise serializers.ValidationError("Account is closed.")

    return iban


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    src = serializers.CharField(max_length=10, validators=[validate_account])
    dest = serializers.CharField(max_length=10, validators=[validate_account])
    amount = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ('url', 'src', 'dest', 'amount', 'timestamp')
        extra_kwargs = {
            'url': {'view_name': 'transactions:transactions-detail'}
        }

    def create(self, validated_data):
        # get accounts by their IBAN
        src = Account.objects.filter(iban=validated_data['src']).first()
        dest = Account.objects.filter(iban=validated_data['dest']).first()

        # create transaction object and proceed
        transaction = Transaction(src=src, dest=dest, amount=validated_data['amount'])
        transaction.proceed()

        return transaction
