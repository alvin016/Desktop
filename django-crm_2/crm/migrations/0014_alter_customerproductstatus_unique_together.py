# Generated by Django 5.2.2 on 2025-06-11 08:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0013_productstatusoption_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='customerproductstatus',
            unique_together={('customer', 'product')},
        ),
    ]
