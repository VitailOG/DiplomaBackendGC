import datetime
import contextlib

from rest_framework.serializers import (
    SerializerMethodField,
    FloatField,
    IntegerField
)

from methodist.constants import SEMESTER_FOR_COURSE
from methodist.models import (
    Student,
    CustomUser,
    Subject,
    Rating,
    Group,
    EducationalProgram,
    ExtraPoints
)
from GradeBookGC_BACKEND.serializers import ModelSerializer
from student.models import StudentSource


class EducationalProgramSerializer(ModelSerializer):
    """ Освітні програми
    """

    class Meta:
        model = EducationalProgram
        fields = ("id", "name")


class ExtraPointsSerializer(ModelSerializer):
    """ Додаткові бали
    """

    class Meta:
        model = ExtraPoints
        fields = (
            'id',
            'semester',
            'point',
            'text',
            'user',
        )


class GroupSerializer(ModelSerializer):
    """ Групи студентів
    """
    semesters = SerializerMethodField()

    class Meta: 
        model = Group
        fields = ("id", "name", "semesters")

    def get_semesters(self, obj):
        with contextlib.suppress(IndexError):
            course = ''.join(filter(str.isdigit, list(obj.name)))[0]
            return SEMESTER_FOR_COURSE[course]


class CustomUserSerializer(ModelSerializer):
    """ Модель Користувачів
    """

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'surname',
            'department'
        )


class SubjectActionSerializer(ModelSerializer):
    """ Модель для створення/редагування предметів
    """

    class Meta:
        model = Subject
        fields = (
            'id',
            'name_subject',
            'group',
            'teachers',
            'hours',
            'loans',
            'semester',
            'final_semester',
            'form_of_control',
            'educational_program',
            'url_on_moodle',
            'finally_subject'
        )
        read_only_fields = ('loans', 'educational_program')


class SubjectWithTeacherSerializer(ModelSerializer):
    """ Вивід предметів із викладачами
    """
    teachers = CustomUserSerializer(many=True)

    class Meta:
        model = Subject
        fields = (
            'id',
            'name_subject',
            'group',
            'teachers',
            'hours',
            'loans',
            'semester',
            'final_semester',
            'form_of_control',
            'educational_program',
            'url_on_moodle',
            'finally_subject'
        )
        read_only_fields = ('loans', 'educational_program')


class SubjectSerializer(ModelSerializer):
    """ Вивід предметів
    """
    group = GroupSerializer()
    educational_program = EducationalProgramSerializer()
    teachers = CustomUserSerializer(many=True)

    class Meta:
        model = Subject
        fields = (
            'id',
            'name_subject',
            'group',
            'teachers',
            'hours',
            'loans',
            'semester',
            'final_semester',
            'form_of_control',
            'educational_program',
            'url_on_moodle',
            'finally_subject'
        )
        read_only_fields = ('loans', 'educational_program')

    def to_representation(self, instance):
        ins = super().to_representation(instance)

        if self.context.get('action') == 'group':
            semester = self.context['query_params'].get('semester')

            ins['students'] = StudentInfoResponseSerializer(
                Student.objects.student_info(group_id=instance.group_id), many=True
            ).data

            ins['ratings'] = RatingSerializer(
                Rating.objects.get_ratings_by_subject(
                    group_id=ins.get('group')['id'],
                    subject_id=instance.id,
                    semester=semester
                ),
                many=True
            ).data

        return ins


class RatingSerializer(ModelSerializer):
    """ Для створення/редагування/вивід у семестрах оцінок
    """

    class Meta:
        model = Rating
        fields = (
            'id',
            'user',
            'subject',
            'date_rating',
            'rating_5',
            'rating_12',
            'retransmission',
            'credited',
            'semester',
            'is_annual_assessment',
            'teacher'
        )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return {key: value for key, value in data.items() if value is not None}


class CommonRatingStudentSerializer(ModelSerializer):
    """ Для виводу загальних оцінок студента плюс - назва предмета і викладачів предмета
    """

    name_subject = SerializerMethodField()
    subject = SubjectWithTeacherSerializer()

    class Meta:
        model = Rating
        fields = (
            'id',
            'user',
            'subject',
            'date_rating',
            'rating_5',
            'rating_12',
            'retransmission',
            'credited',
            'semester',
            'is_annual_assessment',
            'teacher',
            'name_subject',
            'subject'
        )

    def get_name_subject(self, obj):
        return obj.subject.name_subject


# Для студентів
class StudentBaseSerializer(ModelSerializer):
    """ Базовий серіалізатор та для редагування/створення студентів
    """

    course = SerializerMethodField()
    total_rating = FloatField(required=False, read_only=True)

    class Meta:
        model = Student
        fields = (
            'id',
            'user',
            'year_entry',
            'group',
            'educational_program',
            'form_education',
            'course',
            'total_rating'
        )
        read_only_fields = ('user', 'total_rating', 'educational_program')

    def get_course(self, obj):
        days = abs(datetime.date.today() - obj._year_entry).days
        course = (days // 365) + 1
        return course


class StudentInfoResponseSerializer(StudentBaseSerializer):
    """ Більш детальніша інформація про студента
    """

    user = CustomUserSerializer()
    course = SerializerMethodField()
    total_rating = FloatField(required=False, read_only=True)

    class Meta(StudentBaseSerializer.Meta):
        ...


class StudentSourceSerializer(ModelSerializer):
    """ Файли для додаткових балів
    """

    class Meta:
        model = StudentSource
        fields = (
            'id',
            'student',
            'file'
        )


class StudentInfoWithExtraPointsSerializer(StudentInfoResponseSerializer):
    """ Інформація про студента з додатковими бали
    """
    extra_points_students = ExtraPointsSerializer(many=True)
    student_source = StudentSourceSerializer(many=True)

    class Meta(StudentBaseSerializer.Meta):
        fields = StudentBaseSerializer.Meta.fields
        fields += ('extra_points_students', 'student_source')


class StudentCommonRatingSerializer(ModelSerializer):
    """ Інформація про студента з загальним балом та річними оцінками
    """
    user = CustomUserSerializer()
    user_rating = CommonRatingStudentSerializer(many=True)
    total_count = IntegerField(required=False)
    total_sum = IntegerField(required=False)

    class Meta:
        model = Student
        fields = (
            'id',
            'user',
            'year_entry',
            'group',
            'educational_program',
            'form_education',
            'user_rating',
            'total_count',
            'total_sum'
        )


class StudentResponseSerializer(StudentInfoResponseSerializer):
    """ Вся інформація про студента
    """

    group = GroupSerializer()
    educational_program = EducationalProgramSerializer()

    class Meta(StudentInfoResponseSerializer.Meta):
        pass
