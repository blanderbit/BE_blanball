from drf_yasg import openapi

skip_param_query = openapi.Parameter(
    "skipids",
    openapi.IN_QUERY,
    description="This parameter makes it possible to delete \
        entries from the beginning of the list by id. \
        \nQuery example: '1, 2, 3, 4, 5' - 5 entries will be \
        removed from the top of the list",
    type=openapi.TYPE_STRING,
)
point_query = openapi.Parameter(
    "point",
    openapi.IN_QUERY,
    description="This option allows you to sort \
        the list in descending order, starting from \
        the entered coordinate value (longitude, latitude).",
    type=openapi.TYPE_STRING,
)
distance_query = openapi.Parameter(
    "dist",
    openapi.IN_QUERY,
    description="This option allows the user to filter \
    the list of events or the list of users by a radius \
    specified in meters. \nThis parameter cannot work \
    independently, it depends on the point parameter, \
    because it is the point that is considered \
    to be the starting point from which the \
    radius is calculated.\
    \n!!! If you enter a value with a minus sign, the \
    parameter will be simply ignored !!!",
    type=openapi.TYPE_INTEGER,
)
