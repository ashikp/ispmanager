from rest_framework import serializers
from UserController.models import CustomUser, Role

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']  # Add any other fields you need

    def create(self, validated_data):
        # Extract role from validated data, or assign default "Customer" role
        role = validated_data.pop('role', None)
        if role is None:
            role = Role.objects.get(name='Customer')  # Assuming role "Customer" exists
        
        # Create a new CustomUser instance
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Assign the role
        user.role = role
        user.save()
        
        return user