from django.contrib.auth.models import UserManager as DjangoUserManager
from django.db.models import QuerySet

from methodist.constants import TEACHER_GROUP_ID, STUDENT_GROUP_ID
from methodist.models.main import Department


class UserQuerySet(QuerySet):

    def without_group(self, is_exists_student: bool = True):
        return self.filter(
                student__isnull=is_exists_student,
                group_id=STUDENT_GROUP_ID
            )


class UserManager(DjangoUserManager):

    def get_queryset(self):
        return UserQuerySet(
                model=self.model,
                using=self._db
            )

    def without_group_by_department(self, department: Department):
        return self.get_queryset().without_group().filter(department__name=department.name)

    def teachers(self):
        return self.get_queryset().filter(group_id=TEACHER_GROUP_ID)
