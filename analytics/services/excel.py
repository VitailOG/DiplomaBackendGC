import pandas as pd

from asgiref.sync import async_to_sync
from dataclasses import dataclass, field
from functools import cached_property
from typing import NamedTuple, Final, Literal
from pandas.io.excel import ExcelWriter
from pathlib import Path

from django.db.models import QuerySet, Model
from django.contrib.auth import get_user_model

from methodist.models import Student, Rating
from .base import HandlerFactory, BaseCreator, save_message

User = get_user_model()


class SheetType(NamedTuple):
    df: pd.DataFrame
    name: str
    charts: bool = False


METHOD_TYPE = Literal[
    'student',
    'rating'
]


@dataclass
@HandlerFactory.register_handler('excel')
class ExcelCreator(BaseCreator):
    group_id: int
    subject_id: int
    semester: int
    user_id: int
    username: str

    STUDENT_COLUMNS = ["ID", "Логін", "Імя", "Прізвище"]

    METHODS_MAP: Final[dict[str, dict]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        async_to_sync(save_message)(self.user_id, 'File accept')

        self.METHODS_MAP = {
            'student': {
                'qs_method': {
                    "deps": ['group_id'],
                    "name": '_get_student'
                }
            },
            'rating': {
                'qs_method': '_get_ratings'
            },
        }

    @cached_property
    def max_rating(self):
        return 12 if self.semester in (1, 2) else 5

    @property
    def rating_range(self):
        return range(1, self.max_rating + 1)

    def _get_ratings(self) -> QuerySet[Rating]:
        return Rating.objects.get_rating_info(
            subject_id=self.subject_id,
            group_id=self.group_id,
            semester=self.semester,
            rating=self.max_rating
        )

    @staticmethod
    def _get_student(group_id: int) -> QuerySet[Student]:
        return Student.objects.get_values_about_student(group_id=group_id)

    @staticmethod
    def convert_qs_to_df(qs: QuerySet[Model], **kwargs) -> pd.DataFrame:
        return pd.DataFrame(qs).rename(columns=kwargs)

    def _gen_df(self, key: METHOD_TYPE, **kwargs) -> pd.DataFrame:
        name_method = self.METHODS_MAP[key]['qs_method']
        deps = ()

        if isinstance(name_method, dict):
            deps = (getattr(self, _) for _ in name_method['deps'])
            name_method = name_method['name']

        qs = getattr(self, name_method)(*deps)
        df = self.convert_qs_to_df(qs, **kwargs)
        return df

    def __call__(self):
        rating_ua = f"{self.max_rating}-бальний"

        student_col = {"user__username": "Логін", "user__first_name": "Імя", "user__last_name": "Прізвище"}
        student_df = self._gen_df('student', **student_col)

        ratings = pd.DataFrame(self.rating_range, columns=["rating"], dtype='int8')

        rating_col = {
            f"rating_{self.max_rating}": rating_ua,
            "credited": "Перездача", "retransmission": "Зараховано"
        }
        ratings_df = self._gen_df('rating', **rating_col)

        ratings_df[rating_ua] = ratings_df[rating_ua].astype('int8')

        merged_rating = pd.merge(
            ratings, ratings_df, how='left', left_on='rating', right_on=rating_ua
        )

        merged_rating[rating_ua] = merged_rating[rating_ua].fillna(0)

        merged_df = student_df.merge(ratings_df, how='left', left_on='id', right_on='user_id')
        async_to_sync(save_message)(self.user_id, 'Student merged with rating')

        ready_df = merged_rating.groupby(
            [rating_ua, 'rating'], as_index=False
        )[rating_ua].apply(
            self._count_or_null
        ).sort_values(
            by=['rating']
        ).rename(
            columns={"rating": "Оцінки", rating_ua: "Кількість оцінок"}
        ).reset_index(
            drop=True
        )
        async_to_sync(save_message)(self.user_id, 'rating aggregation')

        ready_df.index = self._set_index(ready_df.index.stop)

        common_info_df = merged_df.groupby(
            [rating_ua, 'Перездача'], as_index=False, group_keys=False
        ).agg(
            {rating_ua: ['mean', 'median'], "Перездача": 'sum', 'Зараховано': 'sum'}
        ).rename(columns={rating_ua: 'Оцінки', 'mean': 'Середній бал', 'median': 'Медіана', 'sum': 'Кількість'})
        async_to_sync(save_message)(self.user_id, 'common aggregation')

        merged_df['Перездача'] = merged_df['Перездача'].apply(lambda x: 'Так' if x else 'Ні')
        merged_df['Зараховано'] = merged_df['Зараховано'].apply(lambda x: 'Так' if x else 'Ні')
        merged_df.drop(columns=['user_id'], inplace=True)

        if True in (corr := self._get_or_create_dir()):
            _, filename = corr

            self.save(
                [
                    SheetType(df=ready_df, name='Групування по балам', charts=True),
                    SheetType(merged_df, name='Список групи'),
                    SheetType(df=common_info_df, name='Загальна інформація')
                ],
                filename
            )

    def _get_or_create_dir(self):
        """
            Create dir for analytics files, generate name
            :return tuple bool and file path
        """
        media_analytics_path = Path('media/analytics/')  # root path dir for analytics files

        if not media_analytics_path.exists():  # check exist dir if not create
            media_analytics_path.mkdir(exist_ok=True)

        analytics_dir_for_user = Path.joinpath(media_analytics_path, self.username)  # dir for user

        if not analytics_dir_for_user.exists():  # check exist dir if not create
            analytics_dir_for_user.mkdir(exist_ok=True)

        file_name = f'analytic_for_{self.subject_id}_subject_id_{self.semester}_semester.xlsx'  # name file

        file_path = Path.joinpath(analytics_dir_for_user, file_name)

        return bool(not file_path.exists() or file_path.is_file()), file_path

    @staticmethod
    def _count_or_null(value) -> int:
        if not value.all():
            return 0
        return value.count()

    @staticmethod
    def _set_index(stop: int) -> pd.RangeIndex:
        return pd.RangeIndex(start=1, stop=stop + 1, step=1)

    def save(self, dfs: list[SheetType], file_path: Path) -> None:
        with ExcelWriter(file_path, mode='w', engine='xlsxwriter') as file:
            for df, name, charts in dfs:
                df.to_excel(file, sheet_name=name)

            async_to_sync(save_message)(self.user_id, 'File success generated')
