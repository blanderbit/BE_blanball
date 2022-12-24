from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

skip_param_query = openapi.Parameter(
    "skipids",
    openapi.IN_QUERY,
    description="EN - This parameter makes it possible to delete \
        entries from the beginning of the list by id. \
        \nQuery example: '1, 2, 3, 4, 5' - 5 entries will be \
        removed from the top of the list",
    type=openapi.TYPE_STRING,
)
point_query = openapi.Parameter(
    "point",
    openapi.IN_QUERY,
    description="EN - This option allows you to sort \
        the list in descending order, starting from \
        the entered coordinate value (longitude, latitude).",
    type=openapi.TYPE_STRING,
)
distance_query = openapi.Parameter(
    "dist",
    openapi.IN_QUERY,
    description="EN - This option allows the user to filter \
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


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        """Generate a :class:`.Swagger` object with custom tags"""

        swagger = super().get_schema(request, public)
        swagger.tags = [
            {
                "name": "authentication",
                "description": "EN - a block of endpoints that are fully \
                responsible for user interaction (account creation, \
                registration, password change, mail, login, etc) \
            \nRU - блок конечных точек, которые полностью \
                отвечает за взаимодействие с пользователем (создание учетной записи, \
                регистрация, смена пароля, почта, логин и т.д.) ",
            },
            {
                "name": "events",
                "description": "EN - a block of endpoints that are fully responsible \
                for the operation of events and user interaction with them \
                (creating events, editing, deleting, getting a list and all \
                kinds of filtering , etc) \
            \nRU - блок конечных точек, которые полностью отвечают \
                за работу событий и взаимодействия пользователя с ними\
                (создание событий, редактирование, удаление, получение списка и все\
                виды фильтрации и т.д.)",
            },
            {
                "name": "notifications",
                "description": "EN - a block of endpoints that are fully responsible \
                for notifications and their interaction with users, as well as for \
                changing, getting the current state of tech works and getting the \
                current version of the application \
            \nRU - блок конечных точек, которые полностью отвечают \
                за работу уведомлений и их взаимодействия с пользователями, а также для \
                изменение, получение текущего состояния тех. работ и получение \
                актуальная версия приложения",
            },
            {
                "name": "bugs",
                "description": "EN - a block of endpoints that are fully responsible for  bugs, \
                bug reports and user interaction with them (creating a bug report, getting \
                a list of bugs, filtering, deleting bugs, etc.) \
            \nRU - блок конечных точек, которые полностью ответственны за  ошибки, \
                отчеты об ошибках и взаимодействие пользователя с ними (создание отчета об ошибке, получение\
                список ошибок, фильтрация, удаление ошибок и т.д.) ",
            },
            {
                "name": "cities",
                "description": "EN - a block of endpoints that are responsible for getting cities, \
                getting location by coordinates and coordinates by location \
            \nRU - блок конечных точек, отвечающих за получение городов, \
                получение местоположения по координатам и координат по местоположению ",
            },
            {
                "name": "reviews",
                "description": "EN - a block of endpoints that are fully responsible for working \
                with reviews and user interaction with reviews \
                (creating, deleting, viewing, etc.) \
            \nRU - блок конечных точек, полностью отвечающих за работу\
                с отзывами и взаимодействием пользователей с отзывами \
                (создание, удаление, просмотр и т.д.) ",
            },
        ]
        return swagger
