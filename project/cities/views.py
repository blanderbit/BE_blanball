from typing import Type

from cities.serializers import (
    GetCoordinatesByPlaceNameSerializer,
    GetPlaceNameByCoordinatesSerializer,
)
from cities.services import (
    get_place_name_by_coordinates,
    get_coordinates_by_place_name,
)
from django.conf import settings
from novaposhta import NovaPoshtaApi
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
)

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
        coordinates = get_coordinates_by_place_name(
            place_name=serializer.data["place_name"]
        )
        return Response(coordinates, HTTP_200_OK)


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
        place = get_place_name_by_coordinates(data=serializer.data)
        return Response(place, HTTP_200_OK)


class UkraineAreasList(APIView):
    """
    List of Ukraine areas


    This endpoint allows the user to get
    a list of regions of Ukraine
    """

    def get(self, request: Request) -> Response:
        client = NovaPoshtaApi(api_key=settings.NOVAPOSHTA_API_KEY)
        return Response(client.address.get_areas().json())
