from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Book

User = get_user_model()

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_superuser(**validated_data)
        return user

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
