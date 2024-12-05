from rest_framework import serializers

from .models import Payments, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class UserDetailSerializer(serializers.ModelSerializer):
    payment_history = PaymentsSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "avatar", "country", "payment_history"]
