from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = ('src', 'dest', 'amount', 'timestamp')

    def create(self, validated_data):
        transaction = Transaction.objects.create(
            src=validated_data['src'],
            dest=validated_data['dest'],
            amount=validated_data['amount']
        )

        transaction.src.transfer(transaction.dest, transaction.amount)

        return transaction
