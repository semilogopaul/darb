from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import initialize_payment, verify_payment
from campaigns.models import Campaign
from django.shortcuts import get_object_or_404
from decimal import Decimal

class InitializePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        campaign_id = request.data.get("campaign_id")
        amount = request.data.get("amount")

        campaign = get_object_or_404(Campaign, id=campaign_id)

        if amount > (campaign.goal_amount-campaign.current_amount):
            return Response({"error": "Amount exceeds campaign goal"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.user.email  # Assuming user authentication is handled
        try:
            payment_data = initialize_payment(email, int(amount * 100))  # Convert to kobo
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class VerifyPaymentView(APIView):
    def get(self, request, reference, *args, **kwargs):
        try:
            payment_data = verify_payment(reference)

            if payment_data["data"]["status"] == "success":
                # Process successful payment
                # Example: Update campaign funds
                campaign = get_object_or_404(Campaign, id=request.query_params.get("campaign_id"))
                
                # Convert amount from kobo (integer) to Naira (Decimal)
                amount_paid = Decimal(payment_data["data"]["amount"]) / 100  # Convert to Decimal
                
                campaign.current_amount += amount_paid
                campaign.save()

                return Response({"message": "Payment verified successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Payment not successful"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
