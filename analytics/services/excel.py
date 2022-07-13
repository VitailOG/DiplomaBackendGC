from .base import HandlerFactory, BaseCreator


@HandlerFactory.register_handler('excel')
class ExcelCreator(BaseCreator):
    ...
