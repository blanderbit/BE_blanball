from os import getenv 
from typing import Any, Optional, Union

from cities.constants.errors import (
    NOTHING_FOUND_FOR_USER_REQUEST_ERROR,
)
from config.exceptions import _404
import googlemaps


def get_place_name_by_coordinates(*, data: dict[str, float]) -> Optional[dict[str, str]]:
    """
    Given a dictionary of latitude and longitude coordinates, returns a dictionary
    containing the place name for that location.

    Args:
    data: Dict containing the keys 'lat' and 'lon' representing latitude and longitude coordinates.

    Returns:
    A dictionary containing the place name for the provided coordinates or None if the place name could not be determined.
    """
    gmaps = googlemaps.Client(key=getenv('GOOGLE_MAP_API_KEY'))

    try:
        result = gmaps.reverse_geocode((data['lat'], data['lon']), language='uk')
        if result and result[0]['formatted_address']:
            address_components = result[0]['address_components']
            country = next((component['long_name'] for component in address_components if 'country' in component['types']), '')
            if country.lower() != 'ukraine':
                raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
            region = next((component['long_name'] for component in address_components if 'administrative_area_level_1' in component['types']), '')
            city = next((component['long_name'] for component in address_components if 'locality' in component['types']), '')
            village = next((component['long_name'] for component in address_components if 'sublocality' in component['types']), '')
            district = next((component['long_name'] for component in address_components if 'administrative_area_level_2' in component['types']), '')
            street = next((component['long_name'] for component in address_components if 'route' in component['types']), '')
            return {
                "country": country,
                "region": region,
                "city": city,
                "village": village,
                "district": district,
                "street": street,
            }
        else:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
    except googlemaps.exceptions.Timeout:
        return {"Error": "Error: geocoder service timed out"}
    except googlemaps.exceptions.ApiError as e:
        if "ZERO_RESULTS" in e.args[0]["status"]:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
        else:
            return {"Error": "Error: geocoder service error"}


def get_coordinates_by_place_name(*, place_name: str) -> Optional[dict[str, Union[str, dict[str, str]]]]:
    try:
        gmaps = googlemaps.Client(key=getenv('GOOGLE_MAP_API_KEY'))
        geocode_result = gmaps.geocode(place_name, region="ua")
        if not geocode_result:
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
        location = geocode_result[0]['geometry']['location']
        reverse_geocode_result = gmaps.reverse_geocode((location['lat'], location['lng']))
        address_components = reverse_geocode_result[0]["address_components"]
        country = next((c for c in address_components if "country" in c["types"]), None)
        if not country or country["long_name"].lower() != "ukraine":
            raise _404(detail=NOTHING_FOUND_FOR_USER_REQUEST_ERROR)
        return {
            "coordinates": {
                "lat": location["lat"],
                "lon": location["lng"],
            },
        }
    except googlemaps.exceptions.Timeout:
        return {"Error": "Error: geocoder service timed out"}
    except googlemaps.exceptions.ApiError:
        return {"Error": "Error: geocoder service unavailable"}