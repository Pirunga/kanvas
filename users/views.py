from django.shortcuts import render
from djando.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.serializers import UserSerializer, CourseSerializer
from users.models import Course, Activity
from users.permissions import CoursePermission


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        if User.objects.get(username=data.username):
            return Response(status=status.HTTP_409_CONFLICT)

        user = User.objects.create(**data)

        return Response(status=status.HTTP_201_CREATED)


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated, CoursePermission]

    def get(self):
        ...

    def post(self, request):
        data = request.data

        serializer = CourseSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**serializer.data, user_id=request.user.id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        ...

    def delete(self, request):
        ...


class ActivityView(APIView):
    def post(self, request):
        ...

    def put(self, request):
        ...

    def get(self, request):
        ...
