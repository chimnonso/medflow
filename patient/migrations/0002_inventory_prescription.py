# Generated by Django 4.2.11 on 2024-04-15 16:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medicine_name', models.CharField(max_length=100)),
                ('quantity_in_stock', models.IntegerField()),
                ('expiry_date', models.DateField()),
                ('manufacturer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dosage', models.CharField(max_length=50)),
                ('frequency', models.CharField(max_length=50)),
                ('prescribed_date', models.DateField(default=datetime.date.today)),
                ('medicine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prescriptions', to='patient.inventory')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='patient.patient')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='patient.visit')),
            ],
        ),
    ]
