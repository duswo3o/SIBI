from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        print("userserializer!!!!")
        model = User
        fields = (
            "id",
            "username",
            "email",
            "birthday",
        )
