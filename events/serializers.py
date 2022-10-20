from rest_framework.serializers import ModelSerializer

from events.models import Client


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'sales_contact',
                  'date_created', 'date_updated']
