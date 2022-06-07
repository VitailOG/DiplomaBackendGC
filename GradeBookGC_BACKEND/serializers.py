from rest_framework.serializers import ModelSerializer as RestFrameworkModelSerializer


class ModelSerializer(RestFrameworkModelSerializer):

    @classmethod
    def do(cls, data, context=None, instance=None, partial=False):
        instance = cls(data=data, context=context, instance=instance, partial=partial)
        instance.is_valid(raise_exception=True)
        return instance
