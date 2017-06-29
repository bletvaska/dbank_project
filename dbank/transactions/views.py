from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from account.models import Account
from .forms import TransactionForm
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(Q(src__owner=self.request.user) | Q(dest__owner=self.request.user)).order_by('-timestamp')


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy('transactions_list')
    form_class = TransactionForm

    def get_initial(self):
        return {
            'src': ModelChoiceField(queryset=Account.objects.filter(owner=self.request.user, closed=None),
                                    empty_label='no accounts'),
            'dest': ModelChoiceField(queryset=Account.objects.filter(closed=None), empty_label='no accounts'),
        }

    def form_valid(self, form):
        transaction = form.instance
        account = transaction.src
        account.transfer(transaction.dest, transaction.amount)

        return HttpResponseRedirect(TransactionCreate.success_url)


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
