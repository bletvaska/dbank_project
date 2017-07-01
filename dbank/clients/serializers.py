from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('url', 'first_name', 'last_name', 'email', 'username', 'phone_number')
        extra_kwargs = {
            'url': {'view_name': 'clients:clients-detail'}
        }
