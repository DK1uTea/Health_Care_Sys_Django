from rest_framework import serializers
from .models import User, Role, Permission

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'password', 
                 'first_name', 'last_name', 'phone_number', 'date_of_birth')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user