from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authentication.serializers import UserSerializer

from .models import CartItem, Seller


class SellerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ["user", "company_name", "location"]
        read_only_fields = ["user"]

    def validate(self, data):
        self.user = self.context["request"].user
        try:
            Seller.objects.get(user=self.user)
            raise serializers.ValidationError({"details": "User is already a seller"})
        except ObjectDoesNotExist:
            pass
        return data

    def create(self, validated_data):
        return Seller.objects.create(
            user=self.user,
            company_name=validated_data["company_name"],
            location=validated_data["location"],
        )

    def get_user(self, obj):
        user = UserSerializer(obj.user)
        return user.data


class CartItemListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity"]
        read_only_fields = ["id", "customer"]

    def create(self, validated_data):
        validated_data["customer"] = self.context["request"].user.customer
        obj = CartItem.objects.create(**validated_data)
        return obj


class CartItemUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "customer", "product", "quantity"]
        read_only_fields = ["id", "customer", "product"]
