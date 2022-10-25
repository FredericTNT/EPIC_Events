from django.core.exceptions import ValidationError
from authentication.models import User, Group

SALES = 'Sales'
SUPPORT = 'Support'


def validate_sales_contact(value):
    if type(value) == User:
        team = value.groups
    else:
        team = User.objects.filter(id=value)[0].groups
    query_group = Group.objects.filter(name=SALES)
    if not query_group or team != query_group[0]:
        raise ValidationError(message="Le contact doit appartenir à l'équipe commerciale")


def validate_support_contact(value):
    if type(value) == User:
        team = value.groups
    else:
        team = User.objects.filter(id=value)[0].groups
    query_group = Group.objects.filter(name=SUPPORT)
    if not query_group or team != query_group[0]:
        raise ValidationError(message="Le contact doit appartenir à l'équipe support")
