from typing import Any, Optional, Union

from cities.constants.errors import (
    NOTHING_FOUND_FOR_USER_REQUEST_ERROR,
)
from config.exceptions import _404
from geopy.exc import (
    GeocoderTimedOut,
    GeocoderUnavailable,
)
from geopy.geocoders import Nominatim


def get_place_name_by_coordinates(
    *, data: dict[str, float]
) -> Optional[dict[str, str]]:
    """
    Given a dictionary of latitude and longitude coordinates, returns a dictionary
    containing the place name for that location.

    Args:
    data: Dict containing the keys 'lat' and 'lon' representing latitude and longitude coordinates.

    Returns:
    A dictionary containing the place name for the provided coordinates or None if the place name could not be determined.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    try:
        location = geolocator.reverse(f"{data['lat']}, {data['lon']}", timeout=None)
        if location and location.raw["address"].get("country_code") == "ua":
            return {"data": location.raw["address"]}
        else:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
    except GeocoderTimedOut:
        return {"Error": "Error: geocoder service timed out"}
    except GeocoderUnavailable:
        return {"Error": "Error: geocoder service unavailable"}


def get_coordinates_by_place_name(
    *, place_name: str
) -> Optional[dict[str, Union[str, dict[str, str]]]]:
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(place_name, country_codes="ua", timeout=None)
        if location is None:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
        location = geolocator.reverse(
            f"{location.latitude}, {location.longitude}", timeout=None
        )
        return {
            "data": location.raw["address"],
            "coordinates": {
                "lat": location.latitude,
                "lon": location.longitude,
            },
        }
    except GeocoderTimedOut:
        return {"Error": "Error: geocoder service timed out"}
    except GeocoderUnavailable:
        return {"Error": "Error: geocoder service unavailable"}
