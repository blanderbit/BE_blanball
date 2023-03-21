from config.openapi import (
    concat_search_fields,
    skip_param_query,
    offset_query
)
from drf_yasg import openapi
from notifications.models import Notification


notifications_type_query = openapi.Parameter(
    "type",
    openapi.IN_QUERY,
    description="EN - This option allows you to filter the list of \
    notification by type by selection.\
    \n \
    \n RU - Эта опция позволяет фильтровать список \
    нотификаций по выбору типа.",
    type=openapi.TYPE_STRING,
    enum=[k for k, _ in Notification.Type.choices],
)


notifications_list_query_params: list[openapi.Parameter] = [
    notifications_type_query,
    skip_param_query,
    offset_query,
]