from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import serializers
from .models import User

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        user = User.objects.filter(username=credentials['username']).first()
        
        if user and user.check_password(credentials['password']):
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)
            return {
                'user': user,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        raise serializers.ValidationError('Unable to log in with provided credentials.')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer