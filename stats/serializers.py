from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authentication.serializers import UserSerializer
from store.models import Product

from .models import Customer, Seller


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

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ["user", "address", "wishlist"]
        read_only_fields = ["user"]

    def validate(self, data):
        self.user = self.context["request"].user
        try:
            Customer.objects.get(user=self.user)
            raise serializers.ValidationError({"details": "User is already a customer"})
        except ObjectDoesNotExist:
            pass
        return data

    def create(self, validated_data):
        return Customer.objects.create(
            user=self.user,
            address=validated_data["address"],
            wishlist=validated_data["wishlist"],
        )

    def get_user(self, obj):
        user = UserSerializer(obj.user)
        return user.data


class WishlistProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    def create(self, validated_data):
        product = validated_data["product"]
        customer = self.context["request"].user.customer
        customer.wishlist.add(product)
        return product

