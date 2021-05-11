from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    user_set = UserSerializer(read_only=True, many=True)


class CourseStudentsSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_users_ids(self, value):
        for user_id in value:
            user = User.objects.get(id=user_id)

            if not user:
                raise serializers.ValidationError("Student/Facilitador not found")


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    repo = serializers.CharField()
    grade = serializers.FloatField(default=None)
