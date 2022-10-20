from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import DjangoModelPermissions

from events.models import Client
from events.serializers import ClientSerializer
from events.permissions import IsClientSalesContact


class PresentationView(LoginRequiredMixin, View):
    template_name = 'events/home.html'

    def get(self, request):
        return render(request, self.template_name)


class ClientViewset(ModelViewSet):

    serializer_class = ClientSerializer
    permission_classes = [DjangoModelPermissions, IsClientSalesContact]
    queryset = Client.objects.all()
