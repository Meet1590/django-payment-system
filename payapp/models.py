from django.db import models
from register.models import CustomUser


class Transaction(models.Model):
    source_user_email = models.ForeignKey(CustomUser, related_name='sent_transactions', on_delete=models.CASCADE,
                                          to_field='email')
    destination_user_email = models.ForeignKey(CustomUser, related_name='received_transactions',
                                               on_delete=models.CASCADE, to_field='email')
    amount = models.IntegerField()
    reference = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"From: {self.source_user_email} - To: {self.destination_user_email} - Amount: {self.amount}"
