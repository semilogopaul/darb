from django.urls import path
from .views import CampaignCreateView, LoanCreateView, RepaymentCreateView

urlpatterns = [
    path('create/', CampaignCreateView.as_view(), name='campaign-create'), #supposedly just listcreate/ view since you're getting and posting
    path('loan/', LoanCreateView.as_view(), name='loan-create'),
    path('repayment/', RepaymentCreateView.as_view(), name='repayment-create'),
]
