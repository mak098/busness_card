# Generated by Django 5.0.1 on 2024-04-23 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0006_alter_contact_domicile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='function',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Function'),
        ),
    ]
