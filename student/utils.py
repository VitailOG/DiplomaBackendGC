from gtts import gTTS
from functools import wraps
from pathlib import Path

from rest_framework.exceptions import PermissionDenied
from ninja import Router
from ninja.constants import NOT_SET

from GradeBookGC_BACKEND import settings
from methodist.api.permissions import MethodistPermission
from student.api.permissions import StudentPermission


def router(
        app: Router,
        url_path: str,
        is_methodist: bool = False,
        method: settings.CORS_ALLOW_METHODS = 'GET',
        response=NOT_SET
):
    def decorator(func):
        @getattr(app, method.lower())(f'{url_path}/', response=response)
        @wraps(func)
        def inner(request, *args, **kwargs):

            methodist = MethodistPermission().has_permission(request=request)
            student = StudentPermission().has_permission(request=request)

            if student or bool(is_methodist and methodist):
                return func(request, *args, **kwargs)

            raise PermissionDenied

        return inner
    return decorator


def gen_path(instance, filename):
    suffix = Path(filename).suffix
    type_file = 'audio'

    if suffix != '.mp3':
        type_file = 'image'

    return Path('student', type_file, instance.student.user.username, filename)


def generate_text_to_audio(student, text: str, lang: str = 'uk', slow: bool = False):
    from student.models import StudentSource
    audio = gTTS(text=text, lang=lang, slow=slow)
    return StudentSource().save_audio(file=audio, student=student)

