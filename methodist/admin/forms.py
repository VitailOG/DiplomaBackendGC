from django import forms

from methodist.constants import STUDENT_GROUP_ID
from methodist.models import (
    Subject,
    Rating,
    CustomUser
)


class AbstractAdminForm(forms.ModelForm):
    class Meta:
        field = None
        model = None
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.Meta.field].queryset = CustomUser.objects.teachers()


class SubjectAdminForm(AbstractAdminForm):

    def __init__(self, *args, **kwargs):
        self.Meta.field = 'teachers'
        self.Meta.model = Subject
        super().__init__(*args, **kwargs)


class RatingAdminForm(AbstractAdminForm):

    def __init__(self, *args, **kwargs):
        self.Meta.field = 'teacher'
        self.Meta.model = Rating
        super().__init__(*args, **kwargs)


class StudentAdminForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = CustomUser.objects.filter(group_id=STUDENT_GROUP_ID)
