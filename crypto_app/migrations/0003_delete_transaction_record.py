# Generated by Django 3.2.6 on 2021-09-10 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0002_transaction_record_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction_record',
        ),
    ]
