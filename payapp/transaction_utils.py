from .models import Transaction
from register.models import CustomUser
import requests
import json
from django.http import JsonResponse


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


def currency_conversion_via_api(src_user, dst_user, amount):
    url = 'http://localhost:8000/convert_currency'

    headers = {'Content-Type': 'application/json'}

    req_body = {
        'source_currency': src_user.currency,
        'destination_currency': dst_user.currency,
        'amount': amount,
    }
    try:
        # Make the POST request with the JSON data and headers
        response = requests.post(url, data=req_body)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response content
            response_data = response.json()
            amount = response_data['amount']
            converted_amount = response_data['converted_amount']
            print("hello", amount, converted_amount)
            return JsonResponse(amount, converted_amount)

        else:
            # Return an error response
            return JsonResponse({'error': 'Failed to make POST request'}, status=500)

    except Exception as e:
        # Return an error response
        return JsonResponse({'error': str(e)}, status=500)
