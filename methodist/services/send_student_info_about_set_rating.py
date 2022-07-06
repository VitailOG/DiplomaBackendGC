import contextlib

from typing import Literal
from asgiref.sync import async_to_sync

from bot.main import bot
from methodist.models import Student, Subject, Teacher


MODELS = Literal[
    'student',
    'user',
    'subject'
]


class SendInfoRatingService:

    MODELS = {
        'user': Teacher,
        'student': Student,
        'subject': Subject
    }

    MAIN_CONTENT = " {student}, У Вас - {rating} з {subject}, поставив її {fio}"

    def __init__(
        self, user_id: int, rating: int, teacher_id: int, subject_id: int
    ):
        self.rating = rating

        self.student = self._get_obj(user_id, 'student')
        self.teacher = self._get_obj(teacher_id, 'user')
        self.name_subject = self._get_obj(subject_id, 'subject').name_subject

        self.rating_5_or_12 = '12' if self.get_course(self.student.group.name) == 1 else '5'
        self.message = self._generate_message()

        self.telegram_id = self.student.telegram_id if hasattr(self.student, 'telegram_id') else None

    def __call__(self) -> callable:
        return self._send_message()

    @staticmethod
    def get_course(group_name: str) -> int:
        course = ''.join(filter(str.isdigit, group_name))[0]
        return int(course)

    def _get_obj(self, id: int, model: MODELS) -> Subject | Student | Teacher | None:
        model = self.MODELS[model]
        with contextlib.suppress(getattr(model, 'DoesNotExist')):
            return model.objects.get(id=id)

    def _generate_message(self) -> str:

        message_prefix = self._get_message_prefix(rating=self.rating, rating_5_or_12=self.rating_5_or_12)

        message = message_prefix + self.MAIN_CONTENT.format(
            student=self.student.user.username,
            rating=self.rating,
            subject=self.name_subject,
            fio=self.teacher.get_fio_teacher
        )

        return message

    @staticmethod
    def _get_message_prefix(rating: int, rating_5_or_12: str):
        prefix = {
            "5": {
                (5,): "Хороший результат",
                (3, 4): "Непоганий результат",
                (1, 2): "Вітаю з перездачею",
            },
            "12": {
                (10, 11, 12): "Хороший результат",
                (4, 5, 6, 7, 8, 9): "Непоганий результат",
                (1, 2, 3): "Вітаю з перездачею",
            }
        }
        rat_sys = prefix[rating_5_or_12]
        return rat_sys[list(filter(lambda x: rating in x, rat_sys.keys()))[0]]

    def _send_message(self) -> None:
        if self.telegram_id is not None:
            async_to_sync(bot.send_message)(self.telegram_id, self.message)
