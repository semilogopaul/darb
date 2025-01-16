from django.contrib import admin
from .models import Campaign, Loan, Repayment

admin.site.site_header = "DARB ADMINISTRATION😎🔥🚀"
admin.site.site_title = "Darb Admin Portal"
admin.site.index_title = "Welcome to Darb Administration Portal"

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'founder', 'goal_amount', 'current_amount', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('title', 'founder__username')

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'lender', 'amount', 'created_at')

@admin.register(Repayment)
class RepaymentAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'amount', 'is_fully_repaid', 'created_at')
