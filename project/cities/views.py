from typing import Type

import requests
from cities.constants.errors import (
    NOTHING_FOUND_FOR_USER_REQUEST_ERROR,
)
from cities.serializers import (
    GetCoordinatesByPlaceNameSerializer,
    GetPlaceNameByCoordinatesSerializer,
)
from config.exceptions import _404
from django.conf import settings
from geopy.geocoders import Nominatim
from novaposhta import NovaPoshtaApi
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView


class GetCoordinatesByPlaceName(GenericAPIView):
    """
    Get coordinates by place name

    This endpoint makes it possible to get
    the exact coordinates of a place by name
    Example request:
    {
        "place_name": "Paris"
    }Response:
    {
        "name": "Paris, Île-de-France, France métropolitaine,
            France" - full place name
        "lat": "48.8588897" - latitude
        "lon": "2.3200410217200766" - longitude
    }
    """

    serializer_class: Type[Serializer] = GetCoordinatesByPlaceNameSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(serializer.data["place_name"])
            return Response(
                {
                    "name": location.raw["display_name"],
                    "lat": location.raw["lat"],
                    "lon": location.raw["lon"],
                }
            )
        except AttributeError:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)


class GetPlaceNameByCoordinates(GenericAPIView):
    """
    Get place name by coordinates

    This endpoint allows the user to get the
    name of a point on the map by coordinates
    Example request:
    {
        "lat": "48.8588897" - latitude
        "lon": "2.3200410217200766" - longitude
    }Response:
    {
    "name": "3, Rue Casimir Périer, Quartier des Invalides,
            Paris 7e Arrondissement, Faubourg Saint-Germain, Paris,
            Île-de-France, France métropolitaine, 75007, France" (PARIS)
    }
    """

    serializer_class: Type[Serializer] = GetPlaceNameByCoordinatesSerializer

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.reverse(
                str(serializer.data["lat"]) + "," + str(serializer.data["lon"])
            )
            return Response(
                {
                    "name": location.raw["display_name"],
                }
            )
        except AttributeError:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)


class UkraineAreasList(APIView):
    """
    List of Ukraine areas


    This endpoint allows the user to get
    a list of regions of Ukraine
    """

    def get(self, request: Request) -> Response:
        client = NovaPoshtaApi(api_key=settings.NOVAPOSHTA_API_KEY)
        return Response(client.address.get_areas().json())
