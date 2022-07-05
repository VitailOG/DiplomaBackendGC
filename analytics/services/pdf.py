from . import HandlerFactory


@HandlerFactory.register_handler('pdf')
class PdfService:
    ...
