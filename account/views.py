from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

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


class AccountTransactionListView(ListView):
    model = Transaction
    template_name = 'account/transaction_list.html'

    def get_queryset(self):
        print(self.kwargs.get('account_id'))
        return None


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
