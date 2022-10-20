from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions
from django_filters import rest_framework as df

from events.models import Client
from events.serializers import ClientSerializer
from events.permissions import IsClientSalesContact


class PresentationView(LoginRequiredMixin, View):
    template_name = 'events/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ClientFilter(df.FilterSet):
    min_id = df.NumberFilter(field_name='id', lookup_expr='gte')
    max_id = df.NumberFilter(field_name='id', lookup_expr='lte')

    class Meta:
        model = Client
        fields = ['id', 'last_name', 'first_name', 'sales_contact']


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [DjangoModelPermissions, IsClientSalesContact]
    queryset = Client.objects.all()
    filter_backends = [df.DjangoFilterBackend]
    filterset_class = ClientFilter
