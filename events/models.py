from django.db import models
from authentication.models import User


class Client(models.Model):
    """ Prospect/Client """

    first_name = models.CharField(max_length=25, verbose_name="Prénom")
    last_name = models.CharField(max_length=25, verbose_name="Nom")
    email = models.EmailField(max_length=100, verbose_name="Email")
    phone = models.PositiveBigIntegerField(verbose_name="Téléphone fixe")
    mobile = models.PositiveBigIntegerField(verbose_name="Mobile")
    company_name = models.CharField(max_length=250, verbose_name="Nom de l'entreprise")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)
