from abc import ABCMeta, abstractmethod

from analytics.exceptions import DoesNotRegister


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


class BaseCreator(metaclass=ABCMeta):

    @abstractmethod
    def save(self):
        raise NotImplementedError
