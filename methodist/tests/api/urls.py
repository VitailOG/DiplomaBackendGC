from enum import Enum


class StudentUrl(Enum):
    STUDENT_BASE = '/methodist/student/'
    STUDENT_CREATE = '/methodist/student/create/'
    STUDENT_WITHOUT_GROUP = '/without-group/'


class SubjectUrl(Enum):
    SUBJECT_BASE = '/methodist/subject/'


class RatingUrl(Enum):
    RATING_GROUP = '/methodist/rating/group/'


class GroupUrl(Enum):
    GROUP_BASE = '/methodist/group/'
    CREATE_EXTRA_POINT = '/methodist/group/create_extra_points/'
    UPDATE_EXTRA_POINT = '/methodist/group/update/'
    DETAIL_GROUP = '/methodist/group/detail/'
