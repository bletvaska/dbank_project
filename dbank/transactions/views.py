from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import ModelChoiceField
from django.http import HttpResponseRedirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework import mixins, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from rest_framework.response import Response

from .forms import TransactionForm
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(Q(src__owner=self.request.user) | Q(dest__owner=self.request.user)).order_by(
            '-timestamp')

    def create(self, request, *args, **kwargs):
        response = super(TransactionViewSet, self).create(request, args, kwargs)
        return response

    def retrieve(self, request, pk=None):
        transaction = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = TransactionSerializer(transaction, context={'request': request})
        return Response(serializer.data)


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    success_url = reverse_lazy('transactions:transactions_list')
    form_class = TransactionForm

    def get_initial(self):
        return {
            'src': ModelChoiceField(queryset=Account.objects.filter(owner=self.request.user, closed=None),
                                    empty_label='nothing selected'),
            'dest': ModelChoiceField(queryset=Account.objects.filter(closed=None), empty_label='nothing selected'),
            # 'amount': IntegerField(min_value=1)  # TODO validates the input
        }

    def form_valid(self, form):
        transaction = form.instance
        transaction.proceed()

        messages.info(self.request, f'Transaction of {transaction.amount} was successful.')

        return HttpResponseRedirect(TransactionCreate.success_url)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    ordering = ['-timestamp']
    paginate_by = 15

    def get_queryset(self):
        ordering = self.get_ordering()

        if 'account_id' in self.kwargs:
            account_id = self.kwargs.get('account_id')
            return Transaction.objects.filter(Q(src__id=account_id) | Q(dest__id=account_id)).order_by(*ordering)
        else:
            client = self.request.user
            return Transaction.objects.filter(Q(src__owner=client) | Q(dest__owner=client)).order_by(*ordering)
