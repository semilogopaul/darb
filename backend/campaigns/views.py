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
    serializer_class = RepaymentSerializer

    def get_serializer_context(self):
        # Pass the campaign object into the serializer's context
        campaign_id = self.request.data.get('campaign_id')
        campaign = Campaign.objects.get(id=campaign_id)
        return {'campaign': campaign}

    def perform_create(self, serializer):
        serializer.save()


class CampaignProgressView(generics.RetrieveAPIView):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
