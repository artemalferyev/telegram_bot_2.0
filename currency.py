import requests
from config import CBR_API_URL

def get_exchange_rates():
    try:
        response = requests.get(CBR_API_URL).json()
        rates = {"RUB": 1}
        if "Valute" in response:
            rates["EUR"] = response["Valute"].get("EUR", {}).get("Value", 1)
            rates["USD"] = response["Valute"].get("USD", {}).get("Value", 1)
        return rates
    except Exception as e:
        print(f"Ошибка при получении данных о курсах валют: {e}")
        return {"RUB": 1, "EUR": 1, "USD": 1}

def convert_usd_to_rub(usd_amount):
    try:
        rates = get_exchange_rates()
        usd_rate = rates.get("USD", 1)
        rub_amount = round(usd_amount * usd_rate, 2)
        return rub_amount, usd_rate
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return None, None

def convert_eur_to_rub(eur_amount):
    try:
        rates = get_exchange_rates()
        eur_rate = rates.get("EUR", 1)
        rub_amount = round(eur_amount * eur_rate, 2)
        return rub_amount, eur_rate
    except Exception as e:
        print(f"Ошибка конвертации: {e}")
        return None, None