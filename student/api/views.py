from django.http import HttpResponse
from ninja import Router, UploadedFile, File, Form

from student.services.convert_text_to_audio import ConvertTextToAudioService
from student.utils import router
from student.models import StudentSource
from student.security import AuthBearer
from student.repositories.student_rating_by_semester import StudentRatingRepository
from student.api.schemas import (
    SemestersResponseSchema,
    StudentRatingsResponseSchema,
    ConvertTextToAudioRequestSchema
)
from methodist.models import Rating

api = Router(
    auth=AuthBearer(), tags=['student']
)


@router(
    app=api,
    is_methodist=True,
    url_path='detail',
    response=StudentRatingsResponseSchema
)
def ratings_student_by_semester(
        request,
        semester: int,
        student_id: int = None,
        educational_program_id: int = None
):
    ratings = StudentRatingRepository(
        semester=semester,
        student_id=student_id or request.auth.student.id,
        educational_program_id=educational_program_id or request.auth.student.group.educational_program.id
    )
    return ratings.build_data()


@router(
    app=api,
    url_path='semesters',
    is_methodist=True,
    response=SemestersResponseSchema
)
def semesters_for_student(request, student_id: int = None):
    semesters = Rating.objects.get_semesters_student(student_id=student_id)
    return {"semesters": list(semesters)}


@router(
    app=api,
    url_path='upload-file-for-extra-points',
    method='POST'
)
def upload_file(
        request,
        files: list[UploadedFile] = File(...),
        semester: int = Form(...)
):
    StudentSource.objects.save_files(files=files, semester=semester, student=request.auth.student)


@router(
    app=api,
    url_path='delete-file/{pk}',
    method='POST',
)
def delete_file(request, pk: int):
    StudentSource.objects.filter(id=pk).delete()


@router(
    app=api,
    url_path='convert-text-to-audio',
    method='POST',
)
def convert_text_to_audio(request, data: ConvertTextToAudioRequestSchema):
    res = ConvertTextToAudioService(**data.dict(), student=request.auth.student)()
    response = HttpResponse(res, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="' + res.name + '"'
    return response
