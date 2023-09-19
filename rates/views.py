import requests
from django.shortcuts import render
from django.http import JsonResponse
from currency_converter.settings import API_KEY
from django.http import HttpResponse


def rates(request):
    base = request.GET.get('from', None)
    symbol = request.GET.get('to', None)
    value = request.GET.get('value', None)
    url = f"https://api.currencyfreaks.com/v2.0/rates/latest?"\
        f"apikey={API_KEY}&symbols={symbol}&base={base}"
    response = requests.get(url)

    if not (base or symbol or value):
        return JsonResponse(
            {"details": "Please fill in all required keys: `from`, `to` and `value`"}, 
            status=400
        )

    if response.status_code != 200:
        return JsonResponse({"details": f"`{base}` or `{symbol}` is not correct"}, status=400)

    try:
        float_value = float(value)
    except ValueError:
        return JsonResponse({"details": f"`{value}` should be a float"}, status=400)

    if float_value < 0:
        return JsonResponse({"details": f"`{value}` should be a positive float"}, status=400)

    result = float(response.json()['rates'][symbol]) * float(value)
    response_data = {
        "result": round(result, 2)
    }

    return JsonResponse(response_data)
