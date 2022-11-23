from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from django_filters import rest_framework as df

from events.models import Client, Contract, Event
from events.serializers import ClientSerializer, ContractSerializer, EventSerializer
from events.permissions import IsChangeClientAuthorized, IsChangeContractAuthorized, IsChangeEventAuthorized


class PresentationView(LoginRequiredMixin, View):
    template_name = 'events/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ClientFilter(df.FilterSet):
    min_id = df.NumberFilter(field_name='id', lookup_expr='gte')
    max_id = df.NumberFilter(field_name='id', lookup_expr='lte')
    year_created = df.NumberFilter(field_name='date_created', lookup_expr='year__exact')
    start_last_name = df.CharFilter(field_name='last_name', lookup_expr='istartswith')

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'sales_contact', 'prospect', 'commercial']


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [DjangoModelPermissions, IsChangeClientAuthorized]
    queryset = Client.objects.all()
    filter_backends = [df.DjangoFilterBackend]
    filterset_class = ClientFilter


class ContractFilter(df.FilterSet):
    min_id = df.NumberFilter(field_name='id', lookup_expr='gte')
    max_id = df.NumberFilter(field_name='id', lookup_expr='lte')
    year_created = df.NumberFilter(field_name='date_created', lookup_expr='year__exact')
    month_payment = df.NumberFilter(field_name='payment_due', lookup_expr='month__exact')

    class Meta:
        model = Contract
        fields = ['id', 'amount', 'payment_due', 'status', 'client']


class ContractViewset(ModelViewSet):

    serializer_class = ContractSerializer
    permission_classes = [DjangoModelPermissions, IsChangeContractAuthorized]
    queryset = Contract.objects.all()
    filter_backends = [df.DjangoFilterBackend]
    filterset_class = ContractFilter


class EventFilter(df.FilterSet):
    min_id = df.NumberFilter(field_name='id', lookup_expr='gte')
    max_id = df.NumberFilter(field_name='id', lookup_expr='lte')
    month_event = df.NumberFilter(field_name='date_event', lookup_expr='month__exact')
    year_created = df.NumberFilter(field_name='date_created', lookup_expr='year__exact')
    min_guests = df.NumberFilter(field_name='guests', lookup_expr='gte')
    max_guests = df.NumberFilter(field_name='guests', lookup_expr='lte')

    class Meta:
        model = Event
        fields = ['id', 'date_event', 'status', 'support_contact', 'contract']


class EventViewset(ModelViewSet):

    serializer_class = EventSerializer
    permission_classes = [DjangoModelPermissions, IsChangeEventAuthorized]
    queryset = Event.objects.all()
    filter_backends = [df.DjangoFilterBackend]
    filterset_class = EventFilter
