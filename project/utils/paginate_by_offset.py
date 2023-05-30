from functools import wraps

from django.conf import settings


def paginate_by_offset(cls: type) -> type:
    original_get_queryset = cls.get_queryset

    @wraps(original_get_queryset)
    def new_get_queryset(self, *args, **kwargs):
        offset = self.request.query_params.get("offset")
        if offset is not None:
            try:
                offset = int(offset)
                if offset < 0:
                    offset = self.pagination_class.page_size
            except ValueError:
                offset = None
        if offset is not None:
            self.pagination_class.page_size = offset
        else:
            self.pagination_class.page_size = settings.PAGINATION_PAGE_SIZE
        return original_get_queryset(self, *args, **kwargs)

    cls.get_queryset = new_get_queryset
    return cls
