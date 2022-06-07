import uuid
import tempfile

from django.core.files import File
from django.db import models

from student.managers.source import StudentSourceManager

from student.utils import gen_path


class StudentSource(models.Model):
    objects = StudentSourceManager()
    student = models.ForeignKey('methodist.Student', on_delete=models.CASCADE, related_name='student_source')
    file = models.FileField(upload_to=gen_path)
    semester = models.PositiveIntegerField(verbose_name='Семестер', null=True)

    def __str__(self):
        return self.student.user.username

    class Meta:
        verbose_name = "Файл користувача"
        verbose_name_plural = "Файли користувача"

    def save_file(self, **kwargs):
        """ Для збереження аудіо
        """
        file = kwargs['file']
        student = kwargs['student']
        with tempfile.TemporaryFile(mode='wb+') as fl:
            file.write_to_fp(fl)
            file_name = f'{uuid.uuid4()}.mp3'
            self.student = student
            self.file.save(file_name, File(file=fl))
        return self.file
