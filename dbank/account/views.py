from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
# Create your views here.
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, TemplateView, FormView
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .forms import TransactionForm
from .models import Client, Account, Transaction
from .serializers import AccountSerializer


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

# class ClientListView(LoginRequiredMixin, ListView):
#     model = Client


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(id=self.request.user.id)


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
        # return HttpResponseRedirect(self.get_success_url())


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


@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
class APIAccountList(generics.ListCreateAPIView):
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)
