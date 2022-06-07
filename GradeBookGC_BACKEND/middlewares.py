from django.http import JsonResponse, HttpResponse
from rest_framework import status


class Process500:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        if request.path.startswith('/admin/'):
            return HttpResponse(
                f'<div style="text-align: center; color: red; font-size: 30px;">'
                f'<p><strong>Помилка із БД 500!!!!</strong></p>'
                f'<strong>{str(exception)}</strong>'
                f'</div>'
            )

        return JsonResponse({
            "error": True,
            "message": str(exception)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
