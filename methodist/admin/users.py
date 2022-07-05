from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from methodist.models import CustomUser, Student
from .filters import StudentWithOutListFilter
from .forms import StudentAdminForm


class StudentTabAdmin(admin.TabularInline):
    model = Student


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """ Class admin for custom model `User`
    """
    list_display = (
        'id',
        'username',
        'full_name_user',
        'group',
        'is_student'
    )

    list_display_links = (
        'id',
        'username',
        'full_name_user',
        'group'
    )

    # inlines = [StudentTabAdmin]

    fieldsets = (
        (_('Головні дані'), {
            'fields': ('username', 'password'),
            'classes': ('collapse',)
        }),
        (_('Додаткові дані'), {
            'fields': ('first_name', 'last_name', 'surname', 'email'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Additional Info'), {
            'fields': (('department', 'group'),),
            'classes': ('collapse',)
        }),
    )

    search_fields = (
        'username',
        'first_name',
        'surname',
        'last_name'
    )

    list_filter = (
        'group',
        'department',
        StudentWithOutListFilter
    )

    # list_per_page = 10

    @admin.display(description="ПІБ")
    def full_name_user(self, obj):
        return f'{obj.surname} {obj.last_name} {obj.first_name}'

    @admin.display(
        boolean=True,
        description="З групою (позначається тільки студентам)"
    )
    def is_student(self, obj):
        return bool(obj.student)

    def get_queryset(self, request):
        queryset = super().get_queryset(
            request
        ).select_related(
            'group'
        ).prefetch_related(
            'student'
        )

        return queryset


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    form = StudentAdminForm

    search_fields = (
        'user__username',
        'user__first_name',
        'user__surname',
        'user__last_name'
    )

    list_display = ("id", "full_name_user", 'group_name', 'update_at')

    list_display_links = ("id", "full_name_user")

    list_filter = ('group', 'group__educational_program')

    # telegram_id read only

    list_per_page = 10

    def get_queryset(self, request):
        queryset = super().get_queryset(
            request
        ).select_related(
            'group',
            'user'
        )

        return queryset

    @admin.display(description="ПІБ")
    def full_name_user(self, obj):
        return f'{obj.user.surname} {obj.user.last_name} {obj.user.first_name}'
