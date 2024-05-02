from django import forms
from .models import Transaction, PaymentRequest


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['destination_user_email', 'amount', 'reference']


class PaymentRequestForm(forms.ModelForm):
    class Meta:
        model = PaymentRequest
        fields = ['recipient', 'amount']
