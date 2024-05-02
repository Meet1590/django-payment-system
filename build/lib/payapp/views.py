from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import django.shortcuts
from django.contrib import messages

from register.models import CustomUser
from .forms import TransactionForm, PaymentRequestForm
from .models import Transaction, PaymentRequest
from .transaction_utils import currency_conversion_via_api


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
            src_user = django.shortcuts.get_object_or_404(CustomUser, email=src_email)
            dst_email = form.cleaned_data["destination_user_email"]
            dst_user = django.shortcuts.get_object_or_404(CustomUser, username=dst_email)
            amount = form.cleaned_data["amount"]

            if (src_user.balance > amount) and isinstance(dst_user, CustomUser):

                converted_amount = amount
                if src_user.currency != dst_user.currency:
                    response =  currency_conversion_via_api(src_user, dst_user, amount)
                    print(response)
                print(amount)
                #deduct from sender
                src_user.balance = src_user.balance - amount
                src_user.save()

                print(converted_amount)
                #increse in receiever
                dst_user.balance = dst_user.balance + converted_amount
                dst_user.save()

                # Save the transaction
                t = Transaction(
                    source_user_email=src_user,
                    destination_user_email=dst_user,
                    amount=amount,
                    currency=src_user.currency
                )
                t.save()
                return render(request, "core/view_transaction.html",
                              {"Account balance": src_user, "dst_points": dst_user})
            else:
                html = '<h3> Please ensure you have sufficient balance and recipient is registered with us!</h3>'
                return render(request, html)
    else:
        form = TransactionForm()

    return render(request, "transactions/make_payment.html", context={
        'form':form
    })


@csrf_exempt
@login_required
def show_balance(request):
    # Add logic to retrieve and display balance information
    return render(request, 'core/view_transaction.html', {})


@csrf_exempt
@login_required
def admin(request):
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

@login_required
def dashboard_view(request):
    user = CustomUser.objects.get(username=request.user)
    user_data = {
        'username': user.username,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'currency': user.currency,
        'balance': user.balance
    }
    return render(request, 'core/dashboard.html', context=user_data)



####################################################
#Payment request views


@login_required
def create_payment_request(request):
    users = CustomUser.objects.all()
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            src_username = form.cleaned_data['recipient']
            src_user = django.shortcuts.get_object_or_404(CustomUser, username=src_username)
            payment_request = form.save(commit=False)
            payment_request.sender = request.user.email
            print(payment_request)
            print(payment_request.sender)
            payment_request.save()
            # Send notification to recipient user
            messages.success(request, 'Payment request sent successfully!')
            return redirect('pending_requests')
    else:
        form = PaymentRequestForm()
    return render(request, 'transactions/create_payment_request.html', {'form': form, 'users': users})

def list_pending_requests(request):
    print(request.user)
    pending_requests = PaymentRequest.objects.filter(sender=request.user, status='pending')
    return render(request, 'transactions/list_pending_request.html', {'pending_requests': pending_requests})

def handle_response_to_request(request, request_id):
    payment_request = PaymentRequest.objects.get(pk=request_id)
    if request.method == 'POST':
        action = request.POST.get('action')  # 'accept' or 'reject'
        if action == 'accept':
            payment_request.status = 'accepted'
            # Process payment and update balances
            # Send notification to sender user
        elif action == 'reject':
            payment_request.status = 'rejected'
            # Send notification to sender user
        payment_request.save()
        return redirect('pending_requests')
    return render(request, 'transactions/handle_pending_request.html', {'payment_request': payment_request})
