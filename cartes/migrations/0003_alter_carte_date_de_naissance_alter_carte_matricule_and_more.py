# Generated by Django 5.0.1 on 2024-03-02 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cartes', '0002_carte_adresse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carte',
            name='date_de_naissance',
            field=models.CharField(blank=True, max_length=20, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='carte',
            name='matricule',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='matricule'),
        ),
        migrations.AlterField(
            model_name='carte',
            name='noms',
            field=models.CharField(blank=True, max_length=30, verbose_name='noms'),
        ),
        migrations.AlterField(
            model_name='carte',
            name='promotion',
            field=models.CharField(blank=True, max_length=30, verbose_name='promotion'),
        ),
    ]
