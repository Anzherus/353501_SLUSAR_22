import requests
from django.core.cache import cache
from django.conf import settings
from decimal import Decimal

def get_exchange_rates():
    """
    Получает курсы валют из API или кэша
    """
    # Проверяем кэш
    cached_rates = cache.get('exchange_rates')
    if cached_rates:
        return cached_rates

    try:
        # Используем бесплатное API
        response = requests.get('https://open.er-api.com/v6/latest/BYN')
        if response.status_code == 200:
            data = response.json()
            rates = {
                'BYN': Decimal('1.0'),  # Базовая валюта (белорусский рубль)
                'USD': Decimal(str(data['rates']['USD'])),
                'EUR': Decimal(str(data['rates']['EUR'])),
                'GBP': Decimal(str(data['rates']['GBP'])),
                'JPY': Decimal(str(data['rates']['JPY'])),
                'CNY': Decimal(str(data['rates']['CNY'])),
            }
            
            # Сохраняем в кэш на 1 час
            cache.set('exchange_rates', rates, 3600)
            return rates
    except Exception as e:
        print(f"Error fetching exchange rates: {e}")
        return None

def convert_price(price_byn, target_currency):
    """
    Конвертирует цену из белорусских рублей в целевую валюту
    """
    rates = get_exchange_rates()
    if not rates:
        return None
    
    # Получаем курс целевой валюты
    target_rate = rates.get(target_currency)
    
    if not target_rate:
        return None
    
    # Конвертируем цену
    price_byn = Decimal(str(price_byn))
    price_target = price_byn * target_rate
    
    return round(price_target, 2) 