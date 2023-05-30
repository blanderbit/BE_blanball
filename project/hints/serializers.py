from typing import Any, Union

from hints.models import Hint
from rest_framework.serializers import (
    ModelSerializer,
)


class HintsListSerializer(ModelSerializer):
    class Meta:
        model: Hint = Hint
        fields: Union[str, list[str]] = "__all__"
