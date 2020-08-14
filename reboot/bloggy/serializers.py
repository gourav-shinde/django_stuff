from rest_framework import serializers
from .models import Post
from custom_user.models import User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields="__all__"

