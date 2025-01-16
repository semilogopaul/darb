from rest_framework import serializers
from .models import Campaign, Loan, Repayment

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'title', 'description', 'goal_amount', 'current_amount', 
                  'interest_rate', 'repayment_period', 'is_approved', 'founder']
        read_only_fields = ['current_amount', 'is_approved', 'founder']

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
    class Meta:
        model = Repayment
        fields = ['id', 'campaign', 'amount', 'is_fully_repaid', 'created_at']
        read_only_fields = ['is_fully_repaid']

    def create(self, validated_data):
        campaign = validated_data['campaign']

        # Ensure repayment does not exceed the remaining amount
        remaining = campaign.remaining_repayment()
        if validated_data['amount'] > remaining:
            raise serializers.ValidationError(f"Repayment exceeds the remaining amount of {remaining}.")

        return super().create(validated_data)
