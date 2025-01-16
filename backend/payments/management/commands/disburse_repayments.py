from django.core.management.base import BaseCommand
from campaigns.models import Campaign

class Command(BaseCommand):
    help = "Disburse repayments to lenders."

    def handle(self, *args, **kwargs):
        # Fetch all campaigns with repayments
        campaigns = Campaign.objects.prefetch_related('repayments', 'loans').all()

        # Filter campaigns that are fully repaid
        fully_repaid_campaigns = [
            campaign for campaign in campaigns if campaign.remaining_repayment() <= 0
        ]

        for campaign in fully_repaid_campaigns:
            total_repayment = campaign.calculate_total_repayment()
            loans = campaign.loans.all()
            total_loans = sum([loan.amount for loan in loans])

            # Disburse repayment to each lender proportionally
            for loan in loans:
                lender_share = (loan.amount / total_loans) * total_repayment
                lender = loan.lender
                lender.balance += lender_share  # Assuming Lender model has a balance field
                lender.save()

                self.stdout.write(
                    f"Disbursed {lender_share:.2f} to Lender {lender.id} from Campaign {campaign.id}"
                )

            # Log completion for the campaign
            self.stdout.write(f"Completed disbursement for Campaign {campaign.id}.")
