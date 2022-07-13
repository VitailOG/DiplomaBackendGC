from typing import Literal, NamedTuple

RATING_SYS = Literal[
    '5',
    '12'
]


class DetailSubjectRatingCount(NamedTuple):
    cnt: int
    rat: int
