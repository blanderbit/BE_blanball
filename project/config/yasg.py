import json

from config.openapi import (
    CustomOpenAPISchemaGenerator,
)
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_current_version_for_swagger():
    with open("./config/config.json", "r") as f:
        json_data = json.load(f)
        return json_data["version"]


schema_view = get_schema_view(
    openapi.Info(
        title="Blanball",
        default_version=get_current_version_for_swagger(),
        license=openapi.License(
            name="Attribution-NonCommercial-ShareAlike 4.0 International"
        ),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)

urlpatterns = [
    path(
        "api/v1/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
