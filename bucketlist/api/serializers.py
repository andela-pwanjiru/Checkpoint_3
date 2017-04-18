from rest_framework.serializers import (ModelSerializer, CharField, EmailField)
from app.models import BucketList, BucketListItem
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.models import User


class UserCreateSerializer(ModelSerializer):
    """Define user serializer fields."""

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        email = data['email']
        user_qs = User.objects.filter(email=email)
        if user_qs.exists():
            raise ValidationError("This email already exists")
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User.objects.create_user(username=username,
            email=email, password=password)
        user_obj.save()
        return validated_data


class BucketlistItemSerializer(ModelSerializer):
    """Define bucketlistitems serializer fields."""

    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'done', 'bucketlist',
                  'date_created', 'date_updated')
        read_only_fields = ('id', 'bucketlist', 'date_created', 'date_updated')


class BucketlistSerializer(ModelSerializer):
    """Define bucketlist serializer fields."""
    items = BucketlistItemSerializer(many=True, read_only=True)

    class Meta:
        model = BucketList
        fields = ('id', 'user', 'name', 'items', 'date_created', 'date_updated')
        read_only_fields = ('user',)


