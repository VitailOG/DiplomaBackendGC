from django.contrib import admin
from django.utils.translation import gettext_lazy as _


WITH = 'З'
WITHOUT = 'Без'


class StudentWithOutListFilter(admin.SimpleListFilter):
    title = _('Визначених студенів')
    parameter_name = 'Визначених студенів'

    def lookups(self, request, model_admin):
        return (
            (WITH, _('з групою')),
            (WITHOUT, _('без групи')),
        )

    def queryset(self, request, queryset):
        if self.value() == WITH:
            return queryset.without_group(is_exists_student=False)
        elif self.value() == WITHOUT:
            return queryset.without_group()
