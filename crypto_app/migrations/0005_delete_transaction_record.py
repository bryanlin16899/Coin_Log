# Generated by Django 3.2.6 on 2021-09-10 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0004_transaction_record'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction_record',
        ),
    ]