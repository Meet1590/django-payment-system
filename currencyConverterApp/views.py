from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@csrf_exempt
def convert_currency(request):
    try:
        if request.method == 'POST':
            #only json data is accepted at this api
            data = json.loads(request.body)   # Get the data from the request object

            source_currency = data.get('source_currency')
            destination_currency = data.get('destination_currency')
            amount = data.get('amount')
            amount = int(amount)
            '''
            print(request)
            data = json.load(request)
            print(data)
            source_currency = data.body['source_currency']
            destination_currency = data.body['destination_currency']
            amount = data.body['amount']
            '''
            #hard coded exchange rates
            exchange_rates = {
                ('USD', 'EUR'): 0.85,
                ('USD', 'GBP'): 0.75,
                ('EUR', 'USD'): 1.18,
                ('EUR', 'GBP'): 0.88,
                ('GBP', 'USD'): 1.33,
                ('GBP', 'EUR'): 1.14
            }
            # Check if exchange rate is available for the provided currencies
            if (source_currency, destination_currency) in exchange_rates:
                rate = exchange_rates[(source_currency, destination_currency)]
                converted_amount = amount * rate
                res = {
                    'source_currency': source_currency,
                    'destination_currency': destination_currency,
                    'amount': amount,
                    'converted_amount': converted_amount
                }
            else:
                res = {'error': 'Conversion not available for provided currencies'}
            return JsonResponse(res) #json response
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid data format provided! API only accepts JSON data'})
