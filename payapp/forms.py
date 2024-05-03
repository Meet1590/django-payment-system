from django import forms
from .models import Transaction, PaymentRequest


# Form to get required data to complete a payment transaction
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['destination_user_email', 'amount', 'reference']


# Form to send Payment request to another registered user.
class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['recipient', 'amount']
