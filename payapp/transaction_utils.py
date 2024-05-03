from .models import Transaction
from register.models import CustomUser
import requests
from django.http import JsonResponse


# Logic to call separately defined REST API
def currency_conversion_via_api(src_user, dst_user, amount):
    url = f'https://127.0.0.1:8000/convert_currency/{src_user}/{dst_user}/{(int(amount))}/'
    print("url ============>", url)

    try:
        # Make the POST request with the JSON data and headers
        response = requests.get(url, verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response content
            response_data = response.json().get('data')
            amount = response_data['amount']
            converted_amount = response_data['converted_amount']
            response = {"amount": amount, "converted_amount": converted_amount}
            return response
        else:
            # Return an error response
            return JsonResponse({'error': 'Failed to make  request'}, status=500)

    except Exception as e:
        print("error ==========>", str(e))
        # Return an error response
        return JsonResponse({'error': str(e)}, status=500)

# Testing url for https
# https://127.0.0.1:8000/convert_currency/EUR/GBP/200/
