from typing import Union

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from rest_framework import serializers


class GetCoordinatesByPlaceNameSerializer(serializers.Serializer):
    place_name: bool = serializers.CharField(max_length=255)

    class Meta:
        fields: Union[str, list[str]] = [
            "place_name",
        ]


class PlaceSerializer(serializers.Serializer):
    place_name: str = serializers.CharField(max_length=255)
    lat: float = serializers.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    lon: float = serializers.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
    )

    class Meta:
        fields = [
            "place_name",
            "lon",
            "lat",
        ]


class GetPlaceNameByCoordinatesSerializer(serializers.Serializer):
    lat: float = serializers.FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    lon: float = serializers.FloatField(
        validators=[
            MinValueValidator(-180),
            MaxValueValidator(180),
        ]
    )

    class Meta:
        fields: Union[str, list[str]] = [
            "lat",
            "lon",
        ]
