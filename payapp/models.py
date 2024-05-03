from django.db import models
from register.models import CustomUser


# Transaction table structure(model), help to track and record transactions
class Transaction(models.Model):
    source_user_email = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE,
                                          to_field='email')
    destination_user_email = models.ForeignKey(CustomUser, related_name='received_transactions',
                                               on_delete=models.CASCADE, to_field='email')
    amount = models.IntegerField()
    inward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    outward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    reference = models.CharField(max_length=50)
    currency_choices = [
        ('GBP', 'British Pound'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices, default='GBP')
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"From: {self.source_user_email} - To: {self.destination_user_email} - Amount: {self.amount}"


# Payment request model that helps to track request between sender and recipient with status updates
class PaymentRequest(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_requests', to_field='email')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_requests',
                                  to_field='email')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    status_choices = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender} - To: {self.recipient} - Amount: {self.amount}"
