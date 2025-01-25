from django.db import models
from users.models import User
from decimal import Decimal

class Campaign(models.Model):
    founder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='campaigns')
    title = models.CharField(max_length=255)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage interest rate")
    repayment_period = models.PositiveIntegerField(help_text="Repayment period in months")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_goal_reached(self):
        return self.current_amount >= self.goal_amount
    
    def calculate_total_repayment(self):
        """Calculate the total repayment amount including interest."""
        interest = (self.goal_amount * self.interest_rate) / 100
        return Decimal(self.goal_amount) + Decimal(interest)

    def remaining_repayment(self):
        """Calculate the remaining repayment amount."""
        total_repayment = self.calculate_total_repayment()
        repaid_amount = sum([repayment.amount for repayment in self.repayments.all()])
        return total_repayment - Decimal(repaid_amount)

    def repayment_progress(self):
        """Calculate the percentage of repayment completed."""
        total_repayment = self.calculate_total_repayment()
        repaid_amount = sum([repayment.amount for repayment in self.repayments.all()])
        if total_repayment == 0:
            return 0
        return (Decimal(repaid_amount) / total_repayment) * 100

    def is_fully_repaid(self):
        """Check if the campaign has been fully repaid."""
        return self.remaining_repayment() <= 0

class Loan(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='loans')
    lender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lender.first_name} loaned {self.amount} to {self.campaign.title}"

class Repayment(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_fully_repaid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Repayment of {self.amount} for {self.campaign.title}"
    
    def save(self, *args, **kwargs):
        """Mark the campaign as fully repaid if repayment is complete."""
        super().save(*args, **kwargs)
        if self.campaign.remaining_repayment() <= 0:
            self.campaign.is_fully_repaid = True
            self.campaign.save()
