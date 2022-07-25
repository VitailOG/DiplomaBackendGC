import asyncio

from beanie import init_beanie
from django.core import management

from django.core.management.base import BaseCommand

from motor import motor_asyncio

from authentication.collections import Message


class Command(BaseCommand):

    def handle(self, *args, **options):
        # self.start()
        management.call_command('runserver')

    async def connect_to_mongodb(self):
        client = motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
        await init_beanie(database=client.db_name, document_models=[Message])

    def start(self):
        asyncio.run(self.connect_to_mongodb())
