from django.db import models
from django.core.validators import RegexValidator
from authentication.models import User


class Client(models.Model):
    """ Prospect/Client """

    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")

    first_name = models.CharField(max_length=25, verbose_name="Prénom")
    last_name = models.CharField(max_length=25, verbose_name="Nom")
    email = models.EmailField(max_length=100, verbose_name="Email")
    phone = models.CharField(validators=[phoneNumberRegex], max_length=16, verbose_name="Téléphone fixe")
    mobile = models.CharField(validators=[phoneNumberRegex], max_length=16, verbose_name="Mobile")
    company_name = models.CharField(max_length=250, verbose_name="Nom de l'entreprise")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    sales_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.last_name


class EventStatus(models.Model):
    """ Statut de l'événement """

    status = models.CharField(max_length=50, verbose_name="Statut")

    def __str__(self):
        return self.status


class Contract(models.Model):
    """ Contrat avec le client """

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant facturé")
    payment_due = models.DateField(verbose_name="Date de règlement")
    status = models.BooleanField(verbose_name="Contrat signé")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id} - {self.client}'


class Event(models.Model):
    """ Evénement contractualisé (identification client via contrat) """

    date_event = models.DateTimeField(verbose_name="Date de l'événement")
    guests = models.PositiveIntegerField(verbose_name="Nombre d'invité")
    notes = models.TextField(max_length=250, blank=True, verbose_name="Notes")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    status = models.ForeignKey(to=EventStatus, on_delete=models.SET_NULL, blank=True, null=True)
    support_contact = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)
    contract = models.OneToOneField(to=Contract, on_delete=models.CASCADE)
