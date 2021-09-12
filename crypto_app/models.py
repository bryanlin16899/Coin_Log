from django.db import models

# Transaction record
class Transaction_record(models.Model):
    TYPE_OF_COINS = [
        ('BTC', 'BTC'),
        ('ETH', 'ETH'),
        ('BNB', 'BNB')
    ]

    TYPE_BUY_SELL = [
        ('buy', 'buy'),
        ('sell', 'sell')
    ]

    # id = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=False)
    buy_or_sell = models.CharField(blank=False, max_length=5, choices=TYPE_BUY_SELL)
    type = models.CharField(max_length=10, choices=TYPE_OF_COINS)
    fee = models.FloatField(max_length=5)
    price = models.FloatField(max_length=10)
    amount = models.FloatField(max_length=10)

    def __str__(self):
        return f"{self.type}/{self.amount}"
