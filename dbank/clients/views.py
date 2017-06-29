from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from dbank.clients.models import Client
from .serializers import ClientSerializer


class ClientViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None, format=None):
        client = get_object_or_404(Client, id=request.user.pk, pk=pk)
        serializer = ClientSerializer(client, context={'request': request})
        return Response(serializer.data)

    def list(self, request):
        client = get_object_or_404(Client, id=request.user.pk)
        serializer = ClientSerializer(client, context={'request': request})
        return Response(serializer.data)