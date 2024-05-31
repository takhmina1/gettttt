# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework import status
# # # from .tasks import fetch_and_update_crypto_prices, fetch_and_update_fiat_exchange_rates
# # # from .serializers import CryptoCurrencySerializer, FiatCurrencySerializer

# # # class UpdateCryptoPricesView(APIView):
# # #     def post(self, request, format=None):
# # #         serializer = CryptoCurrencySerializer(data=request.data, many=True)
# # #         if serializer.is_valid():
# # #             crypto_ids = [crypto['symbol'] for crypto in serializer.validated_data]
# # #             fetch_and_update_crypto_prices.delay(crypto_ids)
# # #             return Response({'status': 'Task initiated'}, status=status.HTTP_202_ACCEPTED)
# # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # # class UpdateFiatExchangeRatesView(APIView):
# # #     def post(self, request, format=None):
# # #         serializer = FiatCurrencySerializer(data=request.data, many=True)
# # #         if serializer.is_valid():
# # #             fiat_symbols = [fiat['symbol'] for fiat in serializer.validated_data]
# # #             fetch_and_update_fiat_exchange_rates.delay(fiat_symbols)
# # #             return Response({'status': 'Task initiated'}, status=status.HTTP_202_ACCEPTED)
# # #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework import status
# # from .tasks import fetch_and_update_crypto_prices, fetch_and_update_fiat_exchange_rates
# # from .serializers import CryptoCurrencySerializer, FiatCurrencySerializer
# # from .models import CryptoCurrency, FiatCurrency  # Предполагается, что модели существуют

# # class UpdateCryptoPricesView(APIView):
# #     """
# #     API-представление для получения и обновления цен на криптовалюты.
# #     """
# #     def get(self, request, format=None):
# #         # Получаем все криптовалюты из базы данных
# #         cryptos = CryptoCurrency.objects.all()
# #         serializer = CryptoCurrencySerializer(cryptos, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
    
# #     def post(self, request, format=None):
# #         # Десериализация и проверка данных запроса
# #         serializer = CryptoCurrencySerializer(data=request.data, many=True)
# #         if serializer.is_valid():
# #             # Извлечение символов криптовалют из проверенных данных
# #             crypto_ids = [crypto['symbol'] for crypto in serializer.validated_data]
# #             # Запуск задачи для получения и обновления цен на криптовалюты
# #             fetch_and_update_crypto_prices.delay(crypto_ids)
# #             # Возвращение ответа, указывающего на то, что задача инициирована
# #             return Response({'status': 'Task initiated'}, status=status.HTTP_202_ACCEPTED)
# #         # Возвращение ответа с ошибкой, если данные недействительны
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class UpdateFiatExchangeRatesView(APIView):
# #     """
# #     API-представление для получения и обновления обменных курсов фиатных валют.
# #     """
# #     def get(self, request, format=None):
# #         # Получаем все фиатные валюты из базы данных
# #         fiats = FiatCurrency.objects.all()
# #         serializer = FiatCurrencySerializer(fiats, many=True)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
    
# #     def post(self, request, format=None):
# #         # Десериализация и проверка данных запроса
# #         serializer = FiatCurrencySerializer(data=request.data, many=True)
# #         if serializer.is_valid():
# #             # Извлечение символов фиатных валют из проверенных данных
# #             fiat_symbols = [fiat['symbol'] for fiat in serializer.validated_data]
# #             # Запуск задачи для получения и обновления обменных курсов фиатных валют
# #             fetch_and_update_fiat_exchange_rates.delay(fiat_symbols)
# #             # Возвращение ответа, указывающего на то, что задача инициирована
# #             return Response({'status': 'Task initiated'}, status=status.HTTP_202_ACCEPTED)
# #         # Возвращение ответа с ошибкой, если данные недействительны
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # class UpdateAllCurrenciesView(APIView):
# #     """
# #     API-представление для получения всех криптовалют и фиатных валют,
# #     а также для обновления их курсов.
# #     """
# #     def get(self, request, format=None):
# #         # Получаем все криптовалюты и фиатные валюты из базы данных
# #         cryptos = CryptoCurrency.objects.all()
# #         fiats = FiatCurrency.objects.all()
# #         crypto_serializer = CryptoCurrencySerializer(cryptos, many=True)
# #         fiat_serializer = FiatCurrencySerializer(fiats, many=True)
# #         return Response({
# #             'cryptocurrencies': crypto_serializer.data,
# #             'fiat_currencies': fiat_serializer.data
# #         }, status=status.HTTP_200_OK)
    
# #     def post(self, request, format=None):
# #         # Десериализация и проверка данных запроса для криптовалют и фиатных валют
# #         crypto_serializer = CryptoCurrencySerializer(data=request.data.get('cryptocurrencies', []), many=True)
# #         fiat_serializer = FiatCurrencySerializer(data=request.data.get('fiat_currencies', []), many=True)
        
# #         if crypto_serializer.is_valid() and fiat_serializer.is_valid():
# #             # Извлечение символов криптовалют и фиатных валют из проверенных данных
# #             crypto_ids = [crypto['symbol'] for crypto in crypto_serializer.validated_data]
# #             fiat_symbols = [fiat['symbol'] for fiat in fiat_serializer.validated_data]
            
# #             # Запуск задач для получения и обновления цен на криптовалюты и обменных курсов фиатных валют
# #             fetch_and_update_crypto_prices.delay(crypto_ids)
# #             fetch_and_update_fiat_exchange_rates.delay(fiat_symbols)
            
# #             # Возвращение ответа, указывающего на то, что задачи инициированы
# #             return Response({'status': 'Tasks initiated'}, status=status.HTTP_202_ACCEPTED)
        
# #         # Возвращение ответа с ошибкой, если данные недействительны
# #         errors = {
# #             'cryptocurrencies': crypto_serializer.errors,
# #             'fiat_currencies': fiat_serializer.errors
# #         }
# #         return Response(errors, status=status.HTTP_400_BAD_REQUEST)








# import httpx
# import asyncio
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .tasks import fetch_and_update_crypto_prices, fetch_and_update_fiat_exchange_rates
# from .serializers import CryptoCurrencySerializer, FiatCurrencySerializer

# # URL и параметры внешнего API для получения данных о криптовалютах и фиатных валютах
# CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
# CRYPTO_API_PARAMS = {
#     'ids': 'bitcoin,ethereum',  # Можно добавить больше идентификаторов криптовалют
#     'vs_currencies': 'usd'
# }

# FIAT_API_URL = "https://data.fx.kg/api/v1/currencies"
# FIAT_API_HEADERS = {
#     'Authorization': 'Bearer xrQq7XzYLGGXvK2ci0X9jhUKRJMvxnFBS9GiLnMAffb77394'
# }

# async def get_crypto_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.get(CRYPTO_API_URL, params=CRYPTO_API_PARAMS)
#         response.raise_for_status()  # Проверка на наличие ошибок
#         data = response.json()
#         return data

# async def get_fiat_data():
#     async with httpx.AsyncClient() as client:
#         response = await client.get(FIAT_API_URL, headers=FIAT_API_HEADERS)
#         response.raise_for_status()  # Проверка на наличие ошибок
#         data = response.json()
#         return data

# class UpdateAllCurrenciesView(APIView):
#     """
#     API-представление для получения всех криптовалют и фиатных валют,
#     а также для обновления их курсов.
#     """
#     async def get(self, request, format=None):
#         # Асинхронно получаем данные о криптовалютах и фиатных валютах из внешнего API
#         crypto_data, fiat_data = await asyncio.gather(get_crypto_data(), get_fiat_data())
        
#         return Response({
#             'cryptocurrencies': crypto_data,
#             'fiat_currencies': fiat_data
#         }, status=status.HTTP_200_OK)
    
#     async def post(self, request, format=None):
#         # Десериализация и проверка данных запроса для криптовалют и фиатных валют
#         crypto_serializer = CryptoCurrencySerializer(data=request.data.get('cryptocurrencies', []), many=True)
#         fiat_serializer = FiatCurrencySerializer(data=request.data.get('fiat_currencies', []), many=True)
        
#         if crypto_serializer.is_valid() and fiat_serializer.is_valid():
#             # Извлечение символов криптовалют и фиатных валют из проверенных данных
#             crypto_ids = [crypto['symbol'] for crypto in crypto_serializer.validated_data]
#             fiat_symbols = [fiat['symbol'] for fiat in fiat_serializer.validated_data]
            
#             # Запуск задач для получения и обновления цен на криптовалюты и обменных курсов фиатных валют
#             fetch_and_update_crypto_prices.delay(crypto_ids)
#             fetch_and_update_fiat_exchange_rates.delay(fiat_symbols)
            
#             # Возвращение ответа, указывающего на то, что задачи инициированы
#             return Response({'status': 'Tasks initiated'}, status=status.HTTP_202_ACCEPTED)
        
#         # Возвращение ответа с ошибкой, если данные недействительны
#         errors = {
#             'cryptocurrencies': crypto_serializer.errors,
#             'fiat_currencies': fiat_serializer.errors
#         }
#         return Response(errors, status=status.HTTP_400_BAD_REQUEST)









import httpx
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import sync_to_async
from .tasks import fetch_and_update_crypto_prices, fetch_and_update_fiat_exchange_rates
from .serializers import CryptoCurrencySerializer, FiatCurrencySerializer

# URL и параметры внешнего API для получения данных о криптовалютах и фиатных валютах
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"
CRYPTO_API_PARAMS = {
    'ids': 'bitcoin,ethereum',  # Можно добавить больше идентификаторов криптовалют
    'vs_currencies': 'usd'
}

FIAT_API_URL = "https://data.fx.kg/api/v1/currencies"
FIAT_API_HEADERS = {
    'Authorization': 'Bearer xrQq7XzYLGGXvK2ci0X9jhUKRJMvxnFBS9GiLnMAffb77394'
}

async def get_crypto_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(CRYPTO_API_URL, params=CRYPTO_API_PARAMS)
        response.raise_for_status()  # Проверка на наличие ошибок
        data = response.json()
        return data

async def get_fiat_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(FIAT_API_URL, headers=FIAT_API_HEADERS)
        response.raise_for_status()  # Проверка на наличие ошибок
        data = response.json()
        return data

class UpdateAllCurrenciesView(APIView):
    """
    API-представление для получения всех криптовалют и фиатных валют,
    а также для обновления их курсов.
    """
    def get(self, request, format=None):
        # Запуск асинхронной задачи и ожидание её завершения
        crypto_data, fiat_data = asyncio.run(self._get_data())
        
        return Response({
            'cryptocurrencies': crypto_data,
            'fiat_currencies': fiat_data
        }, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Десериализация и проверка данных запроса для криптовалют и фиатных валют
        crypto_data = request.data.get('cryptocurrencies', [])
        fiat_data = request.data.get('fiat_currencies', [])
        
        crypto_serializer = CryptoCurrencySerializer(data=crypto_data, many=True)
        fiat_serializer = FiatCurrencySerializer(data=fiat_data, many=True)
        
        if crypto_serializer.is_valid() and fiat_serializer.is_valid():
            # Извлечение символов криптовалют и фиатных валют из проверенных данных
            crypto_ids = [crypto['symbol'] for crypto in crypto_serializer.validated_data]
            fiat_symbols = [fiat['symbol'] for fiat in fiat_serializer.validated_data]
            
            # Запуск задач для получения и обновления цен на криптовалюты и обменных курсов фиатных валют
            fetch_and_update_crypto_prices.delay(crypto_ids)
            fetch_and_update_fiat_exchange_rates.delay(fiat_symbols)
            
            # Возвращение ответа, указывающего на то, что задачи инициированы
            return Response({'status': 'Tasks initiated'}, status=status.HTTP_202_ACCEPTED)
        
        # Возвращение ответа с ошибкой, если данные недействительны
        errors = {
            'cryptocurrencies': crypto_serializer.errors,
            'fiat_currencies': fiat_serializer.errors
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    async def _get_data(self):
        crypto_data = await get_crypto_data()
        fiat_data = await get_fiat_data()
        return crypto_data, fiat_data
