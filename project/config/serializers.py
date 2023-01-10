from typing import Union

from rest_framework.serializers import (
    Serializer,
    ListField,
    IntegerField,
)

class BaseBulkDeleteSerializer(Serializer):
    ids: list[int] = ListField(child=IntegerField(min_value=0))

    class Meta:
        fields: Union[str, list[str]] = [
            "ids",
        ]
