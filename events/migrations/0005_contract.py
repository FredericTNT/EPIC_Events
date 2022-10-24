# Generated by Django 4.1.2 on 2022-10-24 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_client_mobile_alter_client_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Montant facturé')),
                ('payment_due', models.DateField(verbose_name='Date de règlement')),
                ('status', models.BooleanField(verbose_name='Statut paiement')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date de création')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date de modification')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.client')),
            ],
        ),
    ]
