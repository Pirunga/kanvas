from django.shortcuts import render, get_object_or_404
from djando.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from users.serializers import (
    UserSerializer,
    CourseSerializer,
    CourseStudentsSerializer,
    ActivitySerializer,
)
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
    def get(self):
        all_courses = [CourseSerializer(course).data for course in Course.objects.all()]

        return Response(all_courses, status=status.HTTP_200_OK)

    def post(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, CoursePermission]

        data = request.data

        serializer = CourseSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**serializer.data, user_id=request.user.id)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, CoursePermission]

        data = request.data

        course = get_object_or_404(Course, id=data["course_id"])

        serializer = CourseStudentsSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        users_id = serializer.data["users_id"]

        for user in course.user_set.all():
            if user.id not in users_id:
                course.user_set.remove(user)

        course_users_id = [user.id for user in Course.user_set.all()]

        for user_id in users_id:
            if user_id not in course_users_id:
                user = User.objects.get(id=user_id)
                course.user_set.add(user)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if not user.is_staff:
            student_activities = [
                ActivitySerializer(activity).data
                for activity in Activity.objects.filter(user_id=user.id)
            ]

            return Response(student_activities, status=status.HTTP_200_OK)

        all_activities = [
            ActivitySerializer(activity).data for activity in Activity.objects.all()
        ]

        return Response(all_activities, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        serializer = ActivitySerializer(data=data)

        if not serializer:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        activity = Activity.objects.create(repo=data["repo"], user_id=user.id)

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user

        if not user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        activity = get_object_or_404(Activity, id=data["id"])

        activity.grade.add(data["grade"])

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivityFilerByStudent(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id):
        user = request.user

        if not user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            student = User.objects.get(user_id=student_id)

            student_activities = [
                ActivitySerializer(activity).data
                for activity in Activity.objects.get(user_id=student.id)
            ]

            return Response(student_activities, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid user_id."}, status=status.HTTP_404_NOT_FOUND
            )
