# # # from django.urls import path
# # # from .views import UpdateCryptoPricesView, UpdateFiatExchangeRatesView

# # # urlpatterns = [
# # #     path('api/update-crypto-prices/', UpdateCryptoPricesView.as_view(), name='update-crypto-prices'),
# # #     path('api/update-fiat-exchange-rates/', UpdateFiatExchangeRatesView.as_view(), name='update-fiat-exchange-rates'),
# # # ]



# # from django.urls import path
# # from .views import UpdateCryptoPricesView, UpdateFiatExchangeRatesView, UpdateAllCurrenciesView

# # urlpatterns = [
# #     path('update-crypto-prices/', UpdateCryptoPricesView.as_view(), name='update_crypto_prices'),
# #     path('update-fiat-exchange-rates/', UpdateFiatExchangeRatesView.as_view(), name='update_fiat_exchange_rates'),
# #     path('update-all-currencies/', UpdateAllCurrenciesView.as_view(), name='update_all_currencies'),
# # ]




# from django.urls import path
# from .views import UpdateAllCurrenciesView

# urlpatterns = [
#     path('update-all-currencies/', UpdateAllCurrenciesView.as_view(), name='update_all_currencies'),
#     # Другие маршруты
# ]





from django.urls import path
from .views import UpdateAllCurrenciesView

urlpatterns = [
    path('update-all-currencies/', UpdateAllCurrenciesView.as_view(), name='update_all_currencies'),
]
