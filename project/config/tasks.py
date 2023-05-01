from config.celery import app
from django.core.management import call_command


@app.task(
    ignore_result=True,
    time_limit=5,
    soft_time_limit=3,
    default_retry_delay=5,
)
def reset_outstanding_jwt_tokens() -> None:
    call_command('flushexpiredtokens')
