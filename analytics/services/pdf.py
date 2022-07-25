from .base import HandlerFactory, BaseCreator


@HandlerFactory.register_handler('pdf')
class PdfCreator(BaseCreator):

    def save(self):
        raise NotImplementedError

    def __call__(self):
        raise NotImplementedError
