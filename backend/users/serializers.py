from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 
                  'bank_name', 'account_number', 'user_type', 'bvn', 'cac_document' 'balance']
        read_only_fields = ['balance']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            bank_name=validated_data['bank_name'],
            account_number=validated_data['account_number'],
            user_type=validated_data['user_type'],
            bvn=validated_data.get('bvn'),
            cac_document=validated_data.get('cac_document'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
