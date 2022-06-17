import uuid
import tempfile

from django.core.files import File
from django.db import models
from django.utils.timezone import now

from student.managers.source import StudentSourceManager

from student.utils import gen_path


class StudentSource(models.Model):

    class TypeFileChoices(models.TextChoices):
        AUDIO = 'Audio', 'Audio'
        IMAGE = 'Image', 'Image'

    class Meta:
        verbose_name = "Файл користувача"
        verbose_name_plural = "Файли користувача"

    objects = StudentSourceManager()
    student = models.ForeignKey('methodist.Student', on_delete=models.CASCADE, related_name='student_source')
    file = models.FileField(upload_to=gen_path)
    semester = models.PositiveIntegerField(verbose_name='Семестер', null=True)

    type_file = models.CharField(verbose_name='Тип файла', max_length=32, default=TypeFileChoices.AUDIO.value)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.student.user.username

    def save_audio(self, **kwargs):
        """ Для збереження аудіо
        """
        file = kwargs['file']
        student = kwargs['student']
        with tempfile.TemporaryFile(mode='wb+') as fl:
            file.write_to_fp(fl)
            file_name = f'{uuid.uuid4()}.mp3'
            self.student = student
            self.type_file = 'audio'
            self.file.save(file_name, File(file=fl))
        return self.file
