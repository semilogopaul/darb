from rest_framework import generics, permissions
from .models import Campaign, Loan, Repayment
from .serializers import CampaignSerializer, LoanSerializer, RepaymentSerializer

class CampaignCreateView(generics.ListCreateAPIView): #supposedly just campain view since you're getting and posting
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

class RepaymentCreateView(generics.CreateAPIView):
    queryset = Repayment.objects.all()
    serializer_class = RepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
