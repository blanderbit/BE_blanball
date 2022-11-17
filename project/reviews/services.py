from authentication.models import User
from typing import Callable, Any
from django.db.models import QuerySet

from reviews.models import Review
from rest_framework.exceptions import (
    PermissionDenied,
)


def hide_user_reviews(func: Callable[[], QuerySet[Review]]):
    def wrap(self) -> QuerySet[Review]:
        try:
            user: User = User.objects.get(id=self.kwargs["pk"])
            if user.configuration["show_reviews"]:
                return func(self)
            elif user == self.request.user:
                return func(self)
            else:
                raise PermissionDenied()
        except User.DoesNotExist:
            pass
        except KeyError:
            return func(self)

    return wrap
