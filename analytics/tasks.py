from asgiref.sync import async_to_sync
from celery import shared_task

from analytics.exceptions import DoesNotRegister
from analytics.services import HandlerFactory
from analytics.services.base import save_message


@shared_task(
    ignore_result=True
)
def generate_analytics_file(name: str, data: dict):
    try:
        HandlerFactory.handler(name, **data)()
    except DoesNotRegister:
        async_to_sync(save_message)(data['user_id'], f'Type {name} file not generated')
