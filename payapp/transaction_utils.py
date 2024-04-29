from models import Transaction
from register.models import CustomUser


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