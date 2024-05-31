from rest_framework import serializers
from .models import CryptoCurrency, FiatCurrency

class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ['name', 'symbol', 'price_usd']

class FiatCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FiatCurrency
        fields = ['name', 'symbol', 'rate_to_usd']
