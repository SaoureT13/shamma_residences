from rest_framework import serializers
from .models import *


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    reservations = serializers.HyperlinkedModelSerializer(
        many=True, view_name="reservation-detail", source="reservation_set"
    )

    class Meta:
        model = Customer
        fields = [
            "id",
            "email",
            "phone_number",
            "firstname",
            "lastname",
            "reservations",
        ]


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(
        many=True, view_name="room-detail", read_only=True, source="category_set"
    )

    class Meta:
        model = Category
        fields = ["url", "id", "name", "rooms"]


class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    rooms = serializers.HyperlinkedRelatedField(
        many=True, view_name="room-detail", read_only=True, source="departement_set"
    )

    class Meta:
        model = Department
        fields = ["url", "id", "name", "address", "rooms"]


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ["url", "id", "name", "price", "available", "description"]
