from celery import shared_task

from analytics.exceptions import DoesNotRegister
from analytics.services import HandlerFactory


@shared_task(
    ignore_result=True
)
def generate_analytics_file(name: str, **kwargs):
    try:
        HandlerFactory.handler(name, **kwargs)()
    except DoesNotRegister:
        # todo write message to db
        return {"Error": True}
