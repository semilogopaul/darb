from django.urls import path
from .views import CampaignCreateView, LoanCreateView, InitializeRepaymentView, VerifyRepaymentView, CampaignProgressView

urlpatterns = [
    path('create/', CampaignCreateView.as_view(), name='campaign-create'), #supposedly just listcreate/ view since you're getting and posting
    path('loan/', LoanCreateView.as_view(), name='loan-create'),
    path('repayment/initialize/', InitializeRepaymentView.as_view(), name='initialize-repayment'),
    path('repayment/verify/<str:reference>/', VerifyRepaymentView.as_view(), name='verify-repayment'),
    path('campaign/<int:pk>/progress/', CampaignProgressView.as_view(), name='campaign-progress'),
]
