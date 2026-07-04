from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'bio', 'profile_picture']
        read_only_fields = ['id']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

    def create(self, validated_data):
        request = self.context.get('request')
        requested_role = validated_data.pop('role', 'student')
        role = 'student'
        if request and request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin':
            role = requested_role
        password = validated_data.pop('password')
        user = User.objects.create(role=role, **validated_data)
        user.set_password(password)
        user.save()
        return user
