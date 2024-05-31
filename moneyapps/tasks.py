from celery import shared_task
import httpx
from .models import CryptoCurrency, FiatCurrency

@shared_task
def fetch_and_update_crypto_prices(crypto_ids):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': ','.join(crypto_ids),
        'vs_currencies': 'usd'
    }
    response = httpx.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    for crypto_id, values in data.items():
        CryptoCurrency.objects.update_or_create(
            symbol=crypto_id,
            defaults={'price_usd': values['usd']}
        )

@shared_task
def fetch_and_update_fiat_exchange_rates(fiat_symbols):
    url = "https://data.fx.kg/api/v1/currencies"
    headers = {
        'Authorization': 'Bearer xrQq7XzYLGGXvK2ci0X9jhUKRJMvxnFBS9GiLnMAffb77394'
    }
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    for currency in data:
        if currency['code'] in fiat_symbols:
            FiatCurrency.objects.update_or_create(
                symbol=currency['code'],
                defaults={'rate_to_usd': currency['rate']}
            )
