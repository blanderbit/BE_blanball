from typing import Union

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from rest_framework.serializers import (
    CharField,
    FloatField,
    Serializer,
)


class GetCoordinatesByPlaceNameSerializer(Serializer):
    place_name: bool = CharField(max_length=255)

    class Meta:
        fields: Union[str, list[str]] = [
            "place_name",
        ]


class PlaceSerializer(Serializer):
    place_name: str = CharField(max_length=255)
    lat: float = FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    lon: float = FloatField(
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


class GetPlaceNameByCoordinatesSerializer(Serializer):
    lat: float = FloatField(
        validators=[
            MinValueValidator(-90),
            MaxValueValidator(90),
        ]
    )
    lon: float = FloatField(
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
