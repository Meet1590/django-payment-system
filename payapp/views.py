from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Q

from register.models import CustomUser
from . import models
from .forms import TransactionForm
from .models import Transaction


@csrf_exempt
@login_required
@transaction.atomic
def make_payment(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            src_email = request.user.email
            print(src_email)
            src_user = get_object_or_404(models.CustomUser, email=src_email)
            dst_email = form.cleaned_data["destination_user_email"]
            print(dst_email.email)
            dst_user = get_object_or_404(models.CustomUser, username=dst_email)
            amount = form.cleaned_data["amount"]

            #deduct from sender
            src_user.balance = src_user.balance - amount
            src_user.save()

            #increse in receiever
            dst_user.balance = dst_user.balance + amount
            dst_user.save()

            # Save the transaction
            t = Transaction(
                source_user_email=src_user,
                destination_user_email=dst_user,
                amount=amount
            )
            t.save()
            return render(request, "core/admin.html",
                          {"Account balance": src_user, "dst_points": dst_user})
    else:
        form = TransactionForm()
    return render(request, "transactions/makepayment.html", {"form": form})


@csrf_exempt
@login_required
def show_balance(request):
    # Add logic to retrieve and display balance information
    return render(request, 'core/view_transaction.html', {})


@csrf_exempt
@login_required
def transaction_success(request):
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

    # Pass the dictionaries to the frontend template
    return render(request, 'core/admin.html', {'transactions': transactions_data, 'users': users_data})
    #return render(request, 'core/view_transaction.html')


@login_required
def view_user_transactions(request):
    user = CustomUser.objects.get(email=request.user.email)
    inward_transactions = Transaction.objects.filter(destination_user_email=user.email).order_by('-timestamp')
    outward_transactions = Transaction.objects.filter(source_user_email=user.email).order_by('-timestamp')

    context = {
        'inward_transactions': inward_transactions,
        'outward_transactions': outward_transactions,
        'username': request.user.username,  # Assuming username is the desired username field
    }

    # Render the template with the populated data
    return render(request, 'core/view_transaction.html', context)
