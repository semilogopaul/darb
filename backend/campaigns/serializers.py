from rest_framework import serializers
from .models import Campaign, Loan, Repayment
from decimal import Decimal

class CampaignSerializer(serializers.ModelSerializer):
    total_repayment = serializers.SerializerMethodField()
    remaining_repayment = serializers.SerializerMethodField()
    repayment_progress = serializers.SerializerMethodField()
    funding_progress = serializers.SerializerMethodField()

    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'goal_amount', 'current_amount', 
                  'interest_rate', 'repayment_period', 'is_approved', 'founder', 'total_repayment', 'remaining_repayment', 'repayment_progress', 'funding_progress', 'is_fully_repaid']
        read_only_fields = ['current_amount', 'is_approved', 'founder']

    def get_total_repayment(self, obj):
        return obj.calculate_total_repayment()

    def get_remaining_repayment(self, obj):
        return obj.remaining_repayment()

    def get_repayment_progress(self, obj):
        return obj.repayment_progress()

    def get_funding_progress(self, obj):
        if obj.goal_amount == 0:
            return 0
        return (Decimal(obj.current_amount) / Decimal(obj.goal_amount)) * 100

    def create(self, validated_data):
        validated_data['founder'] = self.context['request'].user
        return super().create(validated_data)

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'campaign', 'lender', 'amount', 'created_at']
        read_only_fields = ['lender']

    def create(self, validated_data):
        validated_data['lender'] = self.context['request'].user
        campaign = validated_data['campaign']

        # Update campaign's current amount
        campaign.current_amount += validated_data['amount']
        campaign.save()

        return super().create(validated_data)
    
    
class RepaymentSerializer(serializers.ModelSerializer):
    campaign_id = serializers.IntegerField(write_only=True)  # Accept campaign ID from the request
    campaign = serializers.StringRelatedField(read_only=True)  # Read-only campaign data

    class Meta:
        model = Repayment
        fields = ['id', 'campaign_id', 'campaign', 'amount', 'created_at']

    def validate_campaign_id(self, value):
        try:
            campaign = Campaign.objects.get(id=value)
        except Campaign.DoesNotExist:
            raise serializers.ValidationError("Campaign does not exist.")
        return value

    def validate_amount(self, value):
        campaign = self.context['campaign']
        remaining = campaign.remaining_repayment()
        if value > remaining:
            raise serializers.ValidationError(f"Amount exceeds the remaining repayment of {remaining}.")
        return value

    def create(self, validated_data):
        campaign = Campaign.objects.get(id=validated_data.pop('campaign_id'))

        # Add the repayment
        repayment = Repayment.objects.create(campaign=campaign, **validated_data)

        # Check if the campaign is fully repaid
        if campaign.remaining_repayment() <= 0:
            campaign.is_fully_repaid = True
            campaign.save()

        return repayment
