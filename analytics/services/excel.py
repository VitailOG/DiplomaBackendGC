import pandas as pd

from pandas.io.excel import ExcelWriter
from pathlib import Path

from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model

from methodist.models import Student, Rating
from .base import HandlerFactory, BaseCreator


User = get_user_model()


@HandlerFactory.register_handler('excel')
class ExcelCreator(BaseCreator):  # todo in celery task

    STUDENT_COLUMNS = ["ID", "Логін", "Імя", "Прізвище"]

    def __init__(self, group_id: int, semester: int, subject_id: int, user: User):
        self.group_id = group_id
        self.semester = semester
        self.subject_id = subject_id
        self.user = user

    @property
    def rating_range(self):
        max_rating = 12 if self.semester in (1, 2) else 5
        return range(1, max_rating + 1)

    def get_ratings(self) -> QuerySet[Rating]:
        return Rating.objects.get_rating_info(
            subject_id=self.subject_id,
            group_id=self.group_id,
            semester=self.semester
        )

    @staticmethod
    def get_student(group_id: int) -> QuerySet[Student]:
        return Student.objects.get_values_about_student(group_id=group_id)

    @staticmethod
    def convert_qs_to_df(qs: QuerySet[Model], **kwargs) -> pd.DataFrame:
        return pd.DataFrame(qs).rename(columns=kwargs)

    def __call__(self):
        # student_col = {"user__username": "Логін", "user__first_name": "Імя", "user__last_name": "Прізвище"}
        # student_qs = self.get_student(self.group_id)
        # student_df = self.convert_qs_to_df(student_qs, **student_col)

        ratings = pd.DataFrame(self.rating_range, columns=["rating"], dtype='int8')

        ratings_df = self.convert_qs_to_df(self.get_ratings())

        ratings_df["rating_5"] = ratings_df["rating_5"].astype('int8')

        merged_rating = pd.merge(
            ratings, ratings_df, how='left', left_on='rating', right_on='rating_5'
        )

        merged_rating['rating_5'] = merged_rating['rating_5'].fillna(0)

        ready_df = merged_rating.groupby(
            ['rating_5', 'rating'], as_index=False
        ).rating_5.apply(
            self.count_or_null
        ).sort_values(
            by=['rating']
        ).rename(
            columns={"rating": "Оцінки", "rating_5": "Кількість оцінок"}
        )

        media_analytics_path = Path('media/analytics/')

        if not media_analytics_path.exists():
            media_analytics_path.mkdir(exist_ok=True)

        analytics_dir_for_user = Path.joinpath(media_analytics_path, self.user.username)

        if not analytics_dir_for_user.exists():
            analytics_dir_for_user.mkdir(exist_ok=True)

        file_name = f'analytic_for_{self.subject_id}_subject_id_{self.semester}_semester.xlsx'

        file_path = Path.joinpath(analytics_dir_for_user, file_name)

        if not file_path.exists():
            self.save(ready_df, file_path)

        elif file_path.is_file():
            self.save(ready_df, file_path)

        # print(r.groupby(['rating_5', 'rating'], as_index=False).agg({"rating": "count"}))
        # merged_df = student_df.merge(ratings_df, how='left', left_on='id', right_on='user_id')

    @staticmethod
    def count_or_null(value) -> int:
        if not value.all():
            return 0
        return value.count()

    def save(self, df: pd.DataFrame, file_path: Path) -> None:
        with ExcelWriter(file_path, mode='w') as file:
            df.to_excel(file, sheet_name='Групування по оцінкам')
