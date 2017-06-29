from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, TemplateView
from rest_framework import status, viewsets, mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Account
from .serializers import AccountSerializer


# class ClientDetailView(LoginRequiredMixin, DetailView):
#     model = Client
#
#     def get_queryset(self):
#         return Client.objects.filter(id=self.request.user.id)


class AccountListView(LoginRequiredMixin, ListView):
    model = Account

    def get_queryset(self):
        return Account.objects.filter(owner=self.request.user)


class AccountCreate(LoginRequiredMixin, CreateView):
    model = Account
    # form_class = AccountForm
    fields = ['iban']
    success_url = reverse_lazy('accounts_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(AccountCreate, self).form_valid(form)




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
        """
        Return all accounts
        :param request:
        :return:
        """
        # queryset = Account.objects.filter(owner=self.request.user)
        serializer = AccountSerializer(self.get_queryset(), context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Returns information about specific accounts

        :param request: the request object
        :param pk: primary key of the accounts
        :return:
        """
        # queryset = Account.objects.filter(owner=self.request.user)
        account = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = AccountSerializer(account, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        data = {'iban': request.data['iban'], 'owner': reverse('client-detail', kwargs={'pk': request.user.id})}
        # accounts = Account(iban=request.data['iban'], owner=request.user)
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





# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
# class TransactionCreateReadView(generics.ListCreateAPIView):
#     serializer_class = TransactionSerializer
#
#     def get_queryset(self):
#         return Transaction.objects.filter(Q(src__owner=self.request.user) | Q(dest__owner=self.request.user)).order_by('-timestamp')