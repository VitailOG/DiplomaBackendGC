from django.db.models import Aggregate
from django.forms import FloatField


def get_ratings_title(rating_sys: int) -> list[str]:
    return [f"{rating_title} {_set_prefix(rating_title)}" for rating_title in range(1, rating_sys + 1)]


def _set_prefix(rating: int) -> str:
    prefix = {
        (1,): "бал",
        (2, 3, 4): "бали",
        (5, 6, 7, 8, 9, 10, 11, 12): "балів",
    }

    key = [pr for pr in list(prefix) if rating in pr][0]
    return prefix[key]


class Percentile(Aggregate):
    function = 'PERCENTILE_CONT'
    name = 'median'
    output_field = FloatField()
    template = "%(function)s (%(percentile)s) WITHIN GROUP (ORDER BY %(expressions)s)"
