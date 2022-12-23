from bugs.models import Bug
from config.openapi import skip_param_query
from drf_yasg import openapi

bugs_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="This option allows you to filter the list of \
        bugs by type by selection.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Bug.Type.choices],
)
bugs_searh_query = openapi.Parameter(
    "search",
    openapi.IN_QUERY,
    description="This option allows you to filter \
        the list of bugs by fields such as:\
        \n'title'",
    type=openapi.TYPE_STRING,
)
bugs_ordering_query = openapi.Parameter(
    "ordering",
    openapi.IN_QUERY,
    description="This option allows you to sort the list of \
        bugs by fields such as: id, -id\
        \nIf you add a minus before the field name, then sorting \
        will be in reverse order.",
    type=openapi.TYPE_STRING,
)

bugs_list_query_params: list[openapi.Parameter] = [
    skip_param_query,
    bugs_searh_query,
    bugs_type_query,
    bugs_ordering_query,
]