from django.db.models import (
    Manager,
    Prefetch,
    Q,
    Case,
    When,
    BooleanField
)

from methodist.constants import OTHER_CONTROL


class SubjectManager(Manager):

    def subjects(self, department):
        """Для виводу предметів"""
        return self.filter(
                educational_program__department=department
            ).prefetch_related(
                Prefetch('teachers')
            ).select_related(
                'group',
                'educational_program'
            ).order_by(
                '-id'
            )

    def names(self, educational_program_department):
        """Вивід імен предметів"""
        return self.filter(
                educational_program__department=educational_program_department
            ).values(
                'name_subject'
            )

    def detail_subject(self, subject_id: int):
        """Детальний педмет"""
        return self.select_related(
                'group',
            ).filter(
                id=subject_id
            ).first()

    def ratings(
            self,
            semester: int,
            student_id: int,
            educational_program_id: int
    ):
        """Оцінки студента по семестрам"""
        from methodist.models import Rating

        query = self.prefetch_related(
                Prefetch(
                    'rating_set',
                    queryset=Rating.objects.filter(
                        user_id=student_id, semester=semester
                    ).annotate(
                        is_annual=Case(
                            When(
                                Q(subject__form_of_control__in=OTHER_CONTROL) | Q(is_annual_assessment=False),
                                then=False
                            ),
                            default=True,
                            output_field=BooleanField()
                        )
                    )
                )
            ).filter(
                Q(semester=semester) | Q(final_semester=semester),
                educational_program_id=educational_program_id
            )

        return query
