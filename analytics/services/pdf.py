from .base import HandlerFactory, BaseCreator


@HandlerFactory.register_handler('pdf')
class PdfCreator(BaseCreator):
    ...
