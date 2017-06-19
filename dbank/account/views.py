from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import AccountSerializer
from .forms import AccountForm
from .models import Client, Account, Transaction


class HomePage(TemplateView):
    template_name = 'homepage.html'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


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
    success_url = reverse_lazy('bank:accounts-list')

    def form_valid(self, form):
        print('juchu')
        return HttpResponseRedirect(self.get_success_url())

    # def get_form_kwargs(self):
    #     kwargs = super(AccountCreate, self).get_form_kwargs()
    #     kwargs['owner'] = self.request.user
    #     return kwargs


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class AccountCreateReadView(ListCreateAPIView):
    serializer_class = AccountSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['src', 'dest', 'amount', ]
    success_url = reverse_lazy('bank:transactions-list')

    def form_valid(self, form):
        print('juchu')
        return None
