import pandas as pd

from dataclasses import dataclass, field
from typing import NamedTuple
from pandas.io.excel import ExcelWriter
from pathlib import Path
from enum import Enum

from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model

from methodist.models import Student, Rating
from .base import HandlerFactory, BaseCreator


User = get_user_model()


class SheetType(NamedTuple):
    df: pd.DataFrame
    name: str


class MethodName(Enum):
    STUDENT = 'student'
    RATING = 'rating'


@dataclass
@HandlerFactory.register_handler('excel')
class ExcelCreator(BaseCreator):
    group_id: int
    subject_id: int
    semester: int
    user: User

    STUDENT_COLUMNS = ["ID", "Логін", "Імя", "Прізвище"]

    METHODS_MAP: dict[str, dict] = field(init=False, default=dict)

    def __post_init__(self):
        self.METHODS_MAP = {
            'student': {
                'qs_method': {
                    "deps": 'group_id',
                    "name": 'get_student'
                },
                'df_method': '',
            },
            'rating': {
                'qs_method': '',
                'df_method': '',
            },
        }

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

    def _gen_df(self, key: str, **kwargs) -> pd.DataFrame:
        name_method = self.METHODS_MAP[key]['qs_method']
        deps = []  # change on tuple

        if isinstance(name_method, dict):
            deps = [getattr(self, name_method['deps'])]
            name_method = name_method['name']

        qs = getattr(self, name_method)(*deps)  # getattr vs methodcall operator
        df = self.convert_qs_to_df(qs, **kwargs)
        return df

    def __call__(self):
        student_col = {"user__username": "Логін", "user__first_name": "Імя", "user__last_name": "Прізвище"}
        # student_qs = self.get_student(self.group_id)
        # student_df = self.convert_qs_to_df(student_qs, **student_col)
        student_df = self._gen_df('student', **student_col)

        ratings = pd.DataFrame(self.rating_range, columns=["rating"], dtype='int8')

        ratings_df = self.convert_qs_to_df(self.get_ratings())
        ratings_df["rating_5"] = ratings_df["rating_5"].astype('int8')

        merged_rating = pd.merge(
            ratings, ratings_df, how='left', left_on='rating', right_on='rating_5'
        )

        merged_rating['rating_5'] = merged_rating['rating_5'].fillna(0)

        merged_df = student_df.merge(ratings_df, how='left', left_on='id', right_on='user_id')

        ready_df = merged_rating.groupby(
            ['rating_5', 'rating'], as_index=False
        ).rating_5.apply(
            self.count_or_null
        ).sort_values(
            by=['rating']
        ).rename(
            columns={"rating": "Оцінки", "rating_5": "Кількість оцінок"}
        ).reset_index(
            drop=True
        )

        ready_df.index = self._set_index(ready_df.index.stop)

        media_analytics_path = Path('media/analytics/')

        if not media_analytics_path.exists():
            media_analytics_path.mkdir(exist_ok=True)

        analytics_dir_for_user = Path.joinpath(media_analytics_path, self.user.username)

        if not analytics_dir_for_user.exists():
            analytics_dir_for_user.mkdir(exist_ok=True)

        file_name = f'analytic_for_{self.subject_id}_subject_id_{self.semester}_semester.xlsx'

        file_path = Path.joinpath(analytics_dir_for_user, file_name)

        if not file_path.exists() or file_path.is_file():
            self.save(
                [
                    SheetType(df=ready_df, name='Групування по балам'), SheetType(merged_df, name='Список групи')
                ],
                file_path
            )

        # merged_df = student_df.merge(ratings_df, how='left', left_on='id', right_on='user_id')

    @staticmethod
    def count_or_null(value) -> int:
        if not value.all():
            return 0
        return value.count()

    @staticmethod
    def _set_index(stop: int) -> pd.RangeIndex:
        return pd.RangeIndex(start=1, stop=stop + 1, step=1)

    def save(self, dfs: list[SheetType], file_path: Path) -> None:
        with ExcelWriter(file_path, mode='w', engine='xlsxwriter') as file:
            for df, name in dfs:
                df.to_excel(file, sheet_name=name)

            # workbook = file.book
            # worksheet = file.sheets['Групування по оцінкам']
            # chart = workbook.add_chart({"type": "line"})
            # max_row, max_col = df.shape

            # chart.add_series({
            #     'categories': ['Групування по оцінкам', 1, 2, 3, 4],
            #     'values': ['Групування по оцінкам', 1, 2, 3, 4],
            #     'line': {'color': 'red'},
            # })

            # chart.add_series({
            #     'values': '=Групування по оцінкам!$A$1:$A$6',
            #     'marker': {
            #         'type': 'square',
            #         'size': 10,
            #         'border': {'color': 'black'},
            #         'fill': {'color': 'red'},
            #     },
            #     'data_labels': {'value': True},
            # })

            # worksheet.insert_chart(3, 5, chart)
