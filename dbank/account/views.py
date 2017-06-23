from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
# Create your views here.
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, TemplateView, FormView
from rest_framework import generics, status, viewsets, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from .forms import TransactionForm
from .models import Client, Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, ClientSerializer


class HomepageView(TemplateView):
    template_name = 'homepage.html'


class DashboardView(TemplateView):
    template_name = 'account/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        user = self.request.user
        context['client_accounts'] = Account.objects.filter(owner=user)[:10]
        context['last_transactions'] = Transaction.objects.filter(Q(src__owner=user) | Q(dest__owner=user)).order_by('-timestamp')[:10]
        return context


# class ClientDetailView(LoginRequiredMixin, DetailView):
#     model = Client
#
#     def get_queryset(self):
#         return Client.objects.filter(id=self.request.user.id)


class AccountListView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    ordering = ['-timestamp']

    def get_queryset(self):
        ordering = self.get_ordering()

        if 'account_id' in self.kwargs:
            account_id = self.kwargs.get('account_id')
            return Transaction.objects.filter(Q(src__id=account_id) | Q(dest__id=account_id)).order_by(*ordering)
        else:
            client = self.request.user
            return Transaction.objects.filter(Q(src__owner=client) | Q(dest__owner=client)).order_by(*ordering)


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    # form_class = AccountForm
    fields = ['iban']
    success_url = reverse_lazy('bank:accounts_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AccountCreate, self).form_valid(form)


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy('bank:transactions_list')
    form_class = TransactionForm

    def get_initial(self):
        return {
            'src': ModelChoiceField(queryset=Account.objects.filter(owner=self.request.user), empty_label='no account'),
            'dest': ModelChoiceField(queryset=Account.objects.all(), empty_label='no account'),
        }

    def form_valid(self, form):
        transaction = form.instance
        account = transaction.src
        account.transfer(transaction.dest, transaction.amount)

        return HttpResponseRedirect(TransactionCreate.success_url)


# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# class AccountCreateReadView(generics.ListCreateAPIView):
#     serializer_class = AccountSerializer
#
#     def get_queryset(self):
#         return Account.objects.filter(owner=self.request.user)
#
#     def create(self, request, *args, **kwargs):
#         data = {'iban': request.data['iban'], 'owner': request.user.id}
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status.HTTP_201_CREATED, headers=headers)


class AccountViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = AccountSerializer
    # queryset = Account.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        # queryset = Account.objects.filter(owner=self.request.user)
        serializer = AccountSerializer(self.get_queryset(), context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # queryset = Account.objects.filter(owner=self.request.user)
        account = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AccountSerializer(account, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = {'iban': request.data['iban'], 'owner': reverse('client-detail', kwargs={'pk': request.user.id})}
        # account = Account(iban=request.data['iban'], owner=request.user)
        serializer = AccountSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        try:
            instance.close()
        except Exception as ex:
            return Response({'detail': str(ex)}, status.HTTP_400_BAD_REQUEST)

        serializer = AccountSerializer(instance, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class ClientViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None, format=None):
        client = get_object_or_404(Client, id=request.user.pk, pk=pk)
        serializer = ClientSerializer(client, context={'request': request})
        return Response(serializer.data)


class TransactionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(Q(src__owner=self.request.user) | Q(dest__owner=self.request.user)).order_by('-timestamp')


# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# class TransactionCreateReadView(generics.ListCreateAPIView):
#     serializer_class = TransactionSerializer
#
#     def get_queryset(self):
#         return Transaction.objects.filter(Q(src__owner=self.request.user) | Q(dest__owner=self.request.user)).order_by('-timestamp')