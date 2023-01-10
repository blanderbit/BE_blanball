from api_keys.models import ApiKey
from config.celery import app


@app.task
def delete_expired_api_keys() -> None:
    ApiKey.get_only_expired().delete()
