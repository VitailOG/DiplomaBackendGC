from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status, serializers

from methodist.constants import STUDENT_GROUP_ID


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'permission': self.user.group.name})

        if self.user.group.id == STUDENT_GROUP_ID:
            if hasattr(self.user, 'student'):
                data.update({'student_id': self.user.student.id})
            else:
                return {
                    "message": f'Профіль для {self.user.username} не створений',
                    "status_code": status.HTTP_401_UNAUTHORIZED
                }

        return data


class ChangePasswordUserSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=32)
    new_password = serializers.CharField(required=True, max_length=32)
