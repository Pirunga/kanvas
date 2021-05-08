from django.shortcuts import render
from djando.contrib.auth.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


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


class LoginView(APIView):
    def post(self, request):
        ...


class CourseView(APIView):
    def get(self):
        ...

    def post(self, request):
        ...

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
