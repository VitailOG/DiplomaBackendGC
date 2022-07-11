import pandas as pd

from .base import HandlerFactory


@HandlerFactory.register_handler('pdf')
class PdfService:
    ...
