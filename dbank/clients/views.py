from accounts.models import Account
from django.db.models import Q
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.models import Client
from transactions.models import Transaction

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


class DashboardView(TemplateView):
    template_name = 'clients/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        user = self.request.user
        context['client_accounts'] = Account.objects.filter(owner=user)[:10]
        context['last_transactions'] = Transaction.objects.filter(Q(src__owner=user) | Q(dest__owner=user)).order_by('-timestamp')[:10]
        return context