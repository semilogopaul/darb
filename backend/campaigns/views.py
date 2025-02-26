from rest_framework import generics, permissions
from .models import Campaign, Loan, Repayment
from .serializers import CampaignSerializer, LoanSerializer, RepaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import uuid
from users.models import User

class CampaignCreateView(generics.ListCreateAPIView): #supposedly just campain view since you're getting and posting
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]


class InitializeRepaymentView(APIView):
    def post(self, request):
        campaign_id = request.data.get("campaign_id")
        amount = request.data.get("amount")
        email = request.user.email  # Ensure user is authenticated

        # Get the campaign
        try:
            campaign = Campaign.objects.get(id=campaign_id)
        except Campaign.DoesNotExist:
            return Response({"error": "Campaign not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if amount exceeds remaining repayment
        remaining = campaign.remaining_repayment()
        if float(amount) > float(remaining):
            return Response({"error": f"Amount exceeds remaining repayment: {remaining}"}, status=400)

        # Generate unique reference for transaction
        reference = str(uuid.uuid4())

        # Paystack API request
        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "email": email,
            "amount": int(float(amount) * 100),  # Convert to kobo
            "reference": reference,
            # "callback_url": f"{settings.FRONTEND_URL}/repayment-success", DON'T FORGET TO ADD THIS
        }
        response = requests.post(url, headers=headers, json=data)
        res_data = response.json()

        if res_data.get("status") is False:
            return Response({"error": "Payment initialization failed"}, status=400)

        # Save repayment record (unverified)
        Repayment.objects.create(
            campaign=campaign,
            amount=amount,
            reference=reference,
            is_verified=False
        )

        return Response({"payment_url": res_data["data"]["authorization_url"], "reference": reference})

class VerifyRepaymentView(APIView):
    def get(self, request, reference):
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        response = requests.get(url, headers=headers)
        res_data = response.json()

        if not res_data.get("status"):
            return Response({"error": "Payment verification failed"}, status=400)

        # Get the repayment
        try:
            repayment = Repayment.objects.get(reference=reference)
        except Repayment.DoesNotExist:
            return Response({"error": "Repayment not found"}, status=404)

        # Mark repayment as verified
        repayment.is_verified = True
        repayment.save()

        # Check if campaign is fully repaid
        campaign = repayment.campaign
        if campaign.remaining_repayment() <= 0:
            campaign.is_fully_repaid = True
            campaign.save()
            self.disburse_to_lenders(campaign)

        return Response({"message": "Repayment verified successfully", "repayment_status": "Completed"})

    def disburse_to_lenders(self, campaign):
        """Disburse the fully repaid amount to lenders."""
        lenders = campaign.donations.values_list("lender", "amount")  # Get all lenders and their contributions
        lender_map = {}  # Dictionary to store lender balances

        # Calculate repayment ratio for each lender
        total_donated = sum(amount for _, amount in lenders)
        for lender_id, amount in lenders:
            repayment_share = (amount / total_donated) * float(campaign.calculate_total_repayment())
            lender_map[lender_id] = repayment_share

        # Update lender balances
        for lender_id, amount in lender_map.items():
            lender = User.objects.get(id=lender_id)  # Assuming User model is used
            lender.balance += amount
            lender.save()


class CampaignProgressView(generics.RetrieveAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
