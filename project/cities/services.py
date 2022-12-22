from typing import Any, Optional, Union

from cities.constants.errors import (
    NOTHING_FOUND_FOR_USER_REQUEST_ERROR,
)
from config.exceptions import _404
from geopy.geocoders import Nominatim


def get_place_name_by_coordinates(*, data: dict[str, Any]) -> Optional[dict[str, str]]:
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(
            str(data["lat"]) + "," + str(data["lon"])
        )
        place_data: dict[str, Any] = geolocator.geocode(location.raw["display_name"], country_codes="ua")
        if place_data != None:
            return {"data": location.raw['address']}
        else: 
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
    except AttributeError:
        raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)


def get_coordinates_by_place_name(*, place_name: str) -> Optional[dict[str, Union[str, dict[str, str]]]]:
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(place_name, country_codes="ua")
        location = geolocator.reverse(
            str(location.raw["lat"]) + "," + str(location.raw["lon"])
        )
        return {
                "data": location.raw["address"],
                "coordinates": {
                    "lat": location.raw["lat"],
                    "lon": location.raw["lon"],
                    }
                }
    except AttributeError:
        raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)