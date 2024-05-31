from django.db import models

class CryptoCurrency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    price_usd = models.DecimalField(max_digits=20, decimal_places=8)

class FiatCurrency(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)
    rate_to_usd = models.DecimalField(max_digits=20, decimal_places=8)
