from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# Create your views here.
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView

from account.models import Client, Account, Transaction


class Hello(View):
    def get(self, request):
        return HttpResponse('hello world')


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


class AccountTransactionListView(ListView):
    model = Transaction
    template_name = 'account/transaction_list.html'
    ordering = ['-timestamp']

    def get_queryset(self):
        account_id = self.kwargs.get('account_id')
        # q1 = Transaction.objects.filter(src=account_id)
        # q2 = Transaction.objects.filter(dest=account_id)
        # return q1 | q2
        return Transaction.objects.extra(where=['src_id={0} or dest_id={0}'.format(account_id)])


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    ordering = ['-timestamp']

    def get_queryset(self):
        if 'account_id' in self.kwargs:
            account_id = self.kwargs.get('account_id')
            return Transaction.objects.extra(where=['src_id={0} or dest_id={0}'.format(account_id)])
        else:
            return Transaction.objects.all()


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['iban', 'owner', ]
    success_url = reverse_lazy('bank:accounts-list')


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['src', 'dest', 'amount', ]
    success_url = reverse_lazy('bank:transactions-list')
