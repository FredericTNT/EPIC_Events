# Generated by Django 4.1.3 on 2022-11-28 11:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import events.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25, verbose_name='Prénom')),
                ('last_name', models.CharField(max_length=25, verbose_name='Nom')),
                ('email', models.EmailField(max_length=100, verbose_name='Email')),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Téléphone fixe')),
                ('mobile', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')], verbose_name='Mobile')),
                ('company_name', models.CharField(max_length=250, verbose_name="Nom de l'entreprise")),
                ('prospect', models.BooleanField(default=True, verbose_name='Prospect')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('commercial', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='convert', to=settings.AUTH_USER_MODEL, validators=[events.validators.validate_sales_contact])),
                ('sales_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, validators=[events.validators.validate_sales_contact])),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Montant facturé')),
                ('payment_due', models.DateField(verbose_name='Date de règlement')),
                ('status', models.BooleanField(verbose_name='Contrat signé')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.client')),
            ],
        ),
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, verbose_name='Statut')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_event', models.DateTimeField(verbose_name="Date de l'événement")),
                ('guests', models.PositiveIntegerField(verbose_name="Nombre d'invité")),
                ('notes', models.TextField(blank=True, max_length=250, verbose_name='Notes')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='events.contract')),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventstatus')),
                ('support_contact', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, validators=[events.validators.validate_support_contact])),
            ],
        ),
    ]
