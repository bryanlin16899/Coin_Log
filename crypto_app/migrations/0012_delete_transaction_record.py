# Generated by Django 3.2.6 on 2021-09-11 04:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crypto_app', '0011_alter_transaction_record_buy_or_sell'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Transaction_record',
        ),
    ]
