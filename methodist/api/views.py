from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from GradeBookGC_BACKEND.viewsets import BaseViewSet
from GradeBookGC_BACKEND.pagination import BasePagination
from methodist.api.permissions import MethodistPermission
from methodist.api import serializers
from methodist import models
from methodist.constants import TEACHER_GROUP_ID
from methodist.filters import StudentFilter, SubjectFilter


class MethodistView:
    permission_classes = [MethodistPermission]


class StudentApi(MethodistView, BaseViewSet):
    """ API для студенів
        Ф-Ї:
            - Створення/Редагування/Видалення студентів
            - Отримання освітніх програм
            - Отримання студентів без групи
            - Отримання років для фільтрів
    """
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    pagination_class = BasePagination
    filterset_class = StudentFilter
    my_tags = ["METHODIST:STUDENT"]
    ordering_fields = [
        'id',
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__surname',
        'group__name',
        'educational_program__name',
        'form_education',
        'year_entry',
    ]
    lookup_field = "pk"

    def get_queryset(self):
        return models.Student.objects.students(department=self.request.user.department)
        # return models.Student.objects.all()

    @action(
        methods=['post'],
        detail=False,
        url_path="create/(?P<user_id>\d+)",
        url_name='create-student'
    )
    def create_student(self, request, *args, **kwargs):
        """Створення студентів"""
        serializer = self.get_serializer().do(data=request.data)
        self.perform_create(serializer, **kwargs)
        return Response({"created": True}, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_create(serializer, **kwargs):
        serializer.save(**kwargs)

    @action(methods=['get'], detail=False, url_path="without-group")
    def get_students_without_group(self, *args, **kwargs):
        """Отримання студентів без групи"""
        students = models.CustomUser.objects.without_group_by_department(department=self.request.user.department)
        data = serializers.CustomUserSerializer(students, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="educational-programs")
    def get_educational_program(self, *args, **kwargs):
        """Отримання освітніх програм по відділенню"""
        educational_programs = models.EducationalProgram.objects.filter(department=self.request.user.department)
        data = serializers.EducationalProgramSerializer(educational_programs, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        serializers_class_map = {
            'default': serializers.StudentResponseSerializer,
            'create_student': serializers.StudentBaseSerializer,
            'update': serializers.StudentBaseSerializer,
        }
        return serializers_class_map.get(self.action, serializers_class_map['default'])

    def update(self, request, *args, **kwargs):
        """Редагування студентів"""
        instance = self.get_object()
        serializer = self.get_serializer().do(data=request.data, instance=instance)
        self.perform_update(serializer)
        data = serializers.StudentResponseSerializer(instance).data
        return Response(data, status=status.HTTP_200_OK)

    @property
    def first_name(self):
        return self.request.query_params.get('first_name')

    @property
    def last_name(self):
        return self.request.query_params.get('last_name')

    @action(methods=['get'], detail=False, url_path='names')
    def names(self, *args, **kwargs):
        """Виведення імен, якщо вказане прізвище то відбувається фільтр по прізвищу"""
        names = models.Student.objects.data_student(
            fio=self.first_name,
            filter_by='first_name',
            department=self.request.user.department
        )
        if self.last_name:
            names = names.filter(user__last_name__icontains=self.last_name)
        return Response(
            data=names,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='last-names')
    def last_names(self, *args, **kwargs):
        """Виведення прізвищ, якщо вказане прізвище то відбувається фільтр по імені"""
        last_names = models.Student.objects.data_student(
            fio=self.last_name,
            filter_by='last_name',
            department=self.request.user.department
        )
        if self.first_name:
            last_names = last_names.filter(user__first_name__icontains=self.first_name)
        return Response(
            data=last_names,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path="years")
    def years_entry(self, *args, **kwargs):
        """Виведення років для фільтрів"""
        years = models.Student.objects.years(department=self.request.user.department)
        return Response(data=years, status=status.HTTP_200_OK)


class SubjectApi(MethodistView, CreateModelMixin, BaseViewSet):
    """ API для предметів
        Ф-Ї:
            - Створення/Видалення/Редагування/Детальних предметів
            - Виведення назв предмет
            - Виведення викладачів
    """
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = SubjectFilter
    pagination_class = BasePagination
    my_tags = ["METHODIST:SUBJECT"]
    ordering_fields = [
        'id',
        'name_subject',
        'group__name',
        'hours',
        'loans',
        'semester',
        'final_semester',
        'educational_program__name',
        'department__name'
    ]

    def get_queryset(self):
        if self.action != 'retrieve':
            return models.Subject.objects.subjects(self.request.user.department)

    def get_serializer_class(self):
        if self.action not in ("retrieve", "list"):
            return serializers.SubjectActionSerializer
        return serializers.SubjectSerializer

    def retrieve(self, request, *args, **kwargs):
        """Виведення дані на окремий предмет"""
        obj = self.get_object()
        return Response(
            {
                'id': obj.id,
                'name': obj.name_subject,
                'initial_semester': obj.semester,
                'last_semester': obj.final_semester,
                'form_of_control': obj.form_of_control,
            },
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        """Редагування предмета"""
        instance = self.get_object()
        serializer = self.get_serializer().do(instance=instance, data=request.data)
        self.perform_update(serializer)
        data = serializers.SubjectSerializer(instance).data
        return Response(data=data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Створення предмета"""
        serializer = self.get_serializer().do(data=request.data)
        self.perform_create(serializer)
        data = serializers.SubjectSerializer(serializer.instance).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='teachers')
    def get_teachers(self, *args, **kwargs):
        """Виведення викладачів"""
        teachers = models.CustomUser.objects.filter(group_id=TEACHER_GROUP_ID)
        data = serializers.CustomUserSerializer(teachers, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='names-subjects')
    def get_names_subjects(self, *args, **kwargs):
        """Виведення імен предметів"""
        names_subjects = models.Subject.objects.names(educational_program_department=self.request.user.department)
        return Response(data=names_subjects, status=status.HTTP_200_OK)


class RatingApi(MethodistView, UpdateModelMixin, CreateModelMixin, GenericViewSet):
    """ API для оцінок
        Ф-Ї:
            - Створення/Редавання оцінок
            - Виведення всіх оцінок і студентів по предмета на висталення семестрових оцінок
    """
    queryset = models.Rating.objects
    serializer_class = serializers.RatingSerializer
    my_tags = ["METHODIST:RATING"]

    @action(
        methods=['get'],
        detail=False,
        url_path='group/(?P<subject_id>\d+)'
    )
    def group(self, *args, **kwargs):
        """Семестрові оцінки"""
        subject = models.Subject.objects.detail_subject(subject_id=kwargs.get('subject_id'))
        data = serializers.SubjectSerializer(subject, context=self.get_serializer_context()).data
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {
            "action": self.action,
            "query_params": self.request.query_params
        }


class GroupApi(MethodistView, ListModelMixin, GenericViewSet):
    """ API для груп
        Ф-Ї:
            - Виведення стипендіальних рейтингів
            - Виведення загальних балів для всієї групи
            - Створення/Редагування/Видалення додаткових балів
    """
    my_tags = ["METHODIST:GROUP"]

    def get_queryset(self):
        return models.Group.objects.filter(educational_program__department=self.request.user.department)

    @action(methods=['get'], detail=True, url_path='detail/(?P<semester>\d+)')
    def detail_group(self, *args, **kwargs): #
        """Стипендіальні рейтенги"""
        bool_value = True if self.request.query_params.get('is_all_students') == "true" else False
        students = models.Student.objects.rating_list(
            group_id=kwargs['pk'],
            semester=kwargs['semester'],
            is_all_students=bool_value
        )
        data = serializers.StudentInfoWithExtraPointsSerializer(students, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='common-ratings-students')
    def common_rating_students(self, *args, **kwargs):
        """Загальні бали в групі"""
        students = models.Student.objects.common_rating_for_students(group_id=kwargs['pk'])
        data = serializers.StudentCommonRatingSerializer(students, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def create_extra_points(self, *args, **kwargs):  #
        """Створення додаткових балів"""
        serializer = self.get_serializer().do(data=self.request.data)
        self.perform_create(serializer=serializer)
        return Response(data=self.get_serializer(serializer.instance).data, status=status.HTTP_201_CREATED)

    @staticmethod
    def perform_create(serializer):
        serializer.save()

    @action(methods=['delete'], detail=False, url_path='delete/(?P<pk>\d+)')
    def delete(self, request, *args, **kwargs):
        """Видалення додаткових балів"""
        instance = get_object_or_404(models.ExtraPoints, id=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_destroy(instance):
        instance.delete()

    @action(methods=['patch'], detail=False, url_path='update/(?P<pk>\d+)')
    def edit(self, request, *args, **kwargs):  #
        """Редагування додаткових балів"""
        instance = get_object_or_404(models.ExtraPoints, id=kwargs['pk'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def perform_update(serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return serializers.GroupSerializer
        return serializers.ExtraPointsSerializer
