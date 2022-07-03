import sys

from typing import NamedTuple
from gtts import gTTS
from functools import wraps
from pathlib import Path
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import PermissionDenied
from ninja import Router, UploadedFile
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
    audio = gTTS(text=text, lang=lang, slow=slow)  # convert text to audio
    return StudentSource().save_audio(file=audio, student=student)  # save file


class BadFile(NamedTuple):
    name: str
    message: str


class SizeResolution(NamedTuple):
    max: int
    min: int


def convert_pdf_to_image(pdf_file):
    ...


def _resize_image(file: UploadedFile, filename: str) -> InMemoryUploadedFile | UploadedFile:
    img = Image.open(file)

    image_size = SizeResolution(*img.size)
    max_size = SizeResolution(max=100, min=100)

    if not (image_size.max > max_size.max or image_size.min > max_size.min):
        return file

    new_img = img.convert('RGB')
    new_img.thumbnail(max_size)
    filestream = BytesIO()
    new_img.save(filestream, 'JPEG', quality=90)
    filestream.seek(0)
    image = InMemoryUploadedFile(
        filestream, 'FileField', filename, 'jpeg/image', sys.getsizeof(filestream), None
    )
    return image


def check_type_file(files: list[UploadedFile]) -> tuple[list[BadFile], list[UploadedFile]]:
    """ Function check file, if file is image continue, if file is pdf convert to image, else pass """

    bad_files = []
    good_files = []

    for file in files:
        file_name = getattr(file, 'name')
        suffix = Path(file_name).suffix

        if suffix == '.pdf':
            good_files.append(file)
            continue

        try:
            image = _resize_image(file=file, filename=file_name)  # check file is image and resize if need
        except UnidentifiedImageError:
            # add file whose type not image and pdf to bad list for show user
            bad_files.append(
                BadFile(name=getattr(file, 'name'), message="File type not image or pdf, convert please file")
            )

        else:
            good_files.append(image)  # add correct file

    return bad_files, good_files
