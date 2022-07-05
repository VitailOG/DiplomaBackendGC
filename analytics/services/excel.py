from . import HandlerFactory


@HandlerFactory.register_handler('excel')
class ExcelService:
    ...
