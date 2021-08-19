from rest_framework import serializers
from users.models import LoginUser
from accounts.models import CustomUser


class HelloSerializer(serializers.Serializer):
    """serializes a name field for testing our api view"""
    name=serializers.CharField(max_length=10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'email', 'mobile_no', 'user_role', 'user_profile', 'is_verified', 'is_deleted', 'updated_on')
        # fields = '__all__'
            # extra_kwargs = {
            #     'password': {
            #         'write_only': True,
            #         'style': {'input_type': 'password'}
            #     }
            # }

    # def create(self, validated_data):
    #         """Create and return a new user"""
    #         user = models.UserProfile.objects.create_user(
    #             email=validated_data['email'],
    #             name=validated_data['name'],
    #             password=validated_data['password']
    #         )

    #         return user
    # def update(self, instance, validated_data):
    #     """Handle updating user account"""
    #     if 'password' in validated_data:
    #         password = validated_data.pop('password')
    #         instance.set_password(password)
 
    #     return super().update(instance, validated_data)
class ProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:

        model = LoginUser
        fields = ('user_id', 'country')
            # extra_kwargs = {
            #     'password': {
            #         'write_only': True,
            #         'style': {'input_type': 'password'}
            #     }
            # }
