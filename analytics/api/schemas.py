from ninja import Schema


class CountRatingSubject(Schema):
    """
        Example
            -> rating sys = 5 (range 1-5) if 12 (range 1-12)
                rating 1 - count 0
                rating 2 - count 3
                ...
    """
    cnt: int
    rat: int


class AnalyticDetailSubjectResponseSchema(Schema):
    cnt_rating: list[CountRatingSubject]
    rating_title: list[str]
