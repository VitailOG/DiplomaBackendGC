from abc import ABCMeta, abstractmethod

from beanie import init_beanie
from motor import motor_asyncio

from analytics.exceptions import DoesNotRegister
from authentication.collections import Message


class HandlerFactory:

    handlers = {}

    @classmethod
    def handler(cls, name: str, *args, **kwargs):
        try:
            ins = cls.handlers[name](*args, **kwargs)
        except KeyError:
            raise DoesNotRegister
        return ins

    @classmethod
    def register_handler(cls, name: str):
        def inner(klass):
            cls.handlers[name] = klass
            return klass
        return inner


async def init_mongo() -> None:
    client = motor_asyncio.AsyncIOMotorClient("mongodb://127.0.0.1:27017")
    await init_beanie(database=client.db_name, document_models=[Message])


async def save_message(user_id: int, message: str) -> None:
    await init_mongo()  # fixme
    message = Message(user_id=user_id, message=message)
    await message.insert()


class BaseCreator(metaclass=ABCMeta):

    @abstractmethod
    def save(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def __call__(self) -> None:
        raise NotImplementedError
