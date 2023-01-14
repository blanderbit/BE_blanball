from typing import Any, Callable

from authentication.models import User
from django.db.models import QuerySet
from rest_framework.exceptions import (
    PermissionDenied,
)
from reviews.models import Review
from config.exceptions import (
    _404
)


def hide_user_reviews(func: Callable[[], QuerySet[Review]]):
    def wrap(self, *args, **kwargs) -> QuerySet[Review]:
        try:
            user: User = User.objects.get(id=self.kwargs["pk"])
            if user.configuration["show_reviews"]:
                return func(self)
            elif user == self.request.user:
                return func(self, *args, **kwargs)
            else:
                raise PermissionDenied()
        except User.DoesNotExist:
            raise _404(object=User)
        except KeyError:
            return func(self, *args, **kwargs)

    return wrap
