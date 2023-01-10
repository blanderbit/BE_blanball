from api_keys.models import ApiKey


def bulk_delete_api_keys(*, ids: dict[str, int]):
    for api_key_id in ids:
        try:
            ApiKey.objects.get(id=api_key_id).delete()
            yield api_key_id
        except ApiKey.DoesNotExist:
            pass
