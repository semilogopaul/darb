from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('founder', 'Founder'),
        ('lender', 'Lender'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # For founder approval

    # Founder-specific fields
    bvn = models.CharField(max_length=11, null=True, blank=True, unique=True)
    cac_document = models.ImageField(upload_to='cac_documents/', null=True, blank=True)

    # Lender-specific fields
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)

    def is_accessible(self):
        if self.user_type == 'founder' and not self.is_approved:
            return False
        return True

    def __str__(self):
        return self.username
