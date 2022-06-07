from django.contrib import admin
from django.contrib.auth.models import Group as DjangoGroup

from methodist.models import (
    Department,
    Permissions,
    Group,
    EducationalProgram,
    Subject,
    Rating,
    ExtraPoints
)
from .forms import SubjectAdminForm, RatingAdminForm


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    search_fields = (
        "name_subject",
        "group__name"
    )

    list_filter = (
        'group',
        'form_of_control',
        'finally_subject'
    )

    list = (
        "id",
        "name_subject",
        "hours",
        "loans",
        "semester",
        "final_semester",
        "form_of_control",
        "finally_subject"
    )

    list_display = list

    list_display_links = list[:-1]

    list_editable = ('finally_subject',)

    list_per_page = 10

    form = SubjectAdminForm


@admin.register(Permissions)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "__str__",
        "is_annual_assessment",
        "rating_5",
        "rating_12",
        "subject_form_of_control"
    )

    @admin.display(description="Форма конролю")
    def subject_form_of_control(self, obj):
        return f'{obj.subject.form_of_control}'

    form = RatingAdminForm

    list_filter = (
        "user__user__username",
        "is_annual_assessment",
        "semester"
    )

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        queryset = super().get_queryset(
            request
        ).select_related(
            'user__user',
            'subject'
        )
        return queryset


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "educational_program")
    list_display_links = ("id", "name", "educational_program")

    list_filter = (
        "educational_program__department",
    )

    @admin.display(description="Відділення")
    def department(self, obj):
        return f'{obj.department.name}'


@admin.register(ExtraPoints)
class ExtraPointAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__")
    list_display_links = ("id", "__str__")


admin.site.register(Department)
admin.site.register(EducationalProgram)
admin.site.unregister(DjangoGroup)
