from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
@api_view(['GET'])
def convert_currency(request, currency1, currency2, amount):
    try:
        if request.method == 'GET':
            #only json data is accepted at this api
            # data = json.loads(request.body)   # Get the data from the request object

            source_currency = currency1
            destination_currency = currency2
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
                return Response({"status_code": status.HTTP_200_OK, 'message': 'Currency Conversion successfully.', 'data': res}, status=status.HTTP_200_OK)
            else:
                # res = {'error': 'Conversion not available for provided currencies'}
                return Response({"status_code": status.HTTP_406_NOT_ACCEPTABLE, 'message': 'Conversion not available for provided currencies.', 'data': {}}, status=status.HTTP_406_NOT_ACCEPTABLE) #json response
    except Exception as e:
        return Response({"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': str(e), 'data': res}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    

