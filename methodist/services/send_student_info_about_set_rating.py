import contextlib

from typing import Literal
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

from bot.main import bot
from methodist.models import Student, Subject


User = get_user_model()

MODELS = Literal[
    'student',
    'user',
    'subject'
]


class SendInfoRatingService:

    MODELS = {
        'user': User,
        'student': Student,
        'subject': Subject
    }

    def __init__(
            self,
            user_id: int,
            rating: int,
            teacher_id: int,
            subject_id: int
    ):
        self.rating = rating

        self.student = self._get_obj(user_id, 'student')
        self.teacher = self._get_obj(teacher_id, 'user')
        self.name_subject = self._get_obj(subject_id, 'subject').name_subject
        self.message = self._generate_message()

        self.rating_5_or_12 = '12' if self.get_course(self.student.group.name) == 1 else '5'
        self.telegram_id = self.student.telegram_id if hasattr(self.student, 'telegram_id') else None

    def __call__(self):
        return self._send_message()

    @staticmethod
    def get_course(group_name: str) -> int:
        course = ''.join(filter(str.isdigit, group_name))[0]
        return int(course)

    def _get_obj(self, id: int, model: MODELS) -> Subject | Student | User | None:
        model = self.MODELS[model]
        with contextlib.suppress(getattr(model, 'DoesNotExist')):
            return model.objects.get(id=id)

    def _generate_message(self):
        return f"{self.student.user.username} - {self.rating}, {self.teacher}"

    def _send_message(self):
        if self.telegram_id is not None:
            async_to_sync(bot.send_message)(self.telegram_id, self.message)  # make celery task
