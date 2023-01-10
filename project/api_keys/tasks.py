from config.celery import app
from api_keys.models import ApiKey

@app.task
def delete_expired_api_keys() -> None:
    ApiKey.get_only_expired().delete()