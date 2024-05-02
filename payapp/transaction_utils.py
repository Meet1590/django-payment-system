from .models import Transaction
from register.models import CustomUser
import requests
import json
from django.http import JsonResponse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def my_view():
    # Query transactions and users
    transactions = Transaction.objects.all()
    users = CustomUser.objects.all()

    # Convert query results into dictionaries
    transactions_data = [{'source_user_email': transaction.source_user_email.email,
                          'destination_user_email': transaction.destination_user_email.email,
                          'amount': transaction.amount,
                          'reference': transaction.reference,
                          'timestamp': transaction.timestamp,
                          'status': transaction.status} for transaction in transactions]

    users_data = [{'email': user.email,
                   'first_name': user.first_name,
                   'last_name': user.last_name,
                   'balance': user.balance} for user in users]
    print(transactions_data)
    print(users_data)
    # Pass the dictionaries to the frontend template
    #return render(request, 'my_template.html', {'transactions': transactions_data, 'users': users_data})
import requests


def currency_conversion_via_api(src_user, dst_user, amount):
    url = f'https://127.0.0.1:8000/convert_currency/{src_user}/{dst_user}/{(int(amount))}/'
    print("url ============>" , url)

    # headers = {'Content-Type': 'application/json'}

    try:
        # Make the POST request with the JSON data and headers
        response = requests.get(url , verify=False)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response content
            response_data = response.json().get('data')
            amount = response_data['amount']
            converted_amount = response_data['converted_amount']
            response = {"amount": amount , "converted_amount" : converted_amount}
            return response
        else:
            # Return an error response
            return JsonResponse({'error': 'Failed to make  request'}, status=500)

    except Exception as e:
        print("error ==========>",str(e))
        # Return an error response
        return JsonResponse({'error': str(e)}, status=500)
# https://127.0.0.1:8000/convert_currency/EUR/GBP/200/