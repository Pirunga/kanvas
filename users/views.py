from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        try:
            user = User.objects.get(username=data["username"])

            return Response(status=status.HTTP_409_CONFLICT)

        except User.DoesNotExist:
            user = User.objects.create_user(**data)

            serializer = UserSerializer(user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [CoursePermission]

    def get(self, request):
        all_courses = [CourseSerializer(course).data for course in Course.objects.all()]

        return Response(all_courses, status=status.HTTP_200_OK)

    def post(self, request):

        data = request.data

        serializer = CourseSerializer(data=data)

        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        course = Course.objects.create(**serializer.data)

        serializer = CourseSerializer(course)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseStudentRegistration(APIView):
    def put(self, request):
        data = request.data

        course = get_object_or_404(Course, id=data["course_id"])

        serializer = CourseStudentsSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        users_id = data.pop("user_ids")

        for user in course.user_set.all():
            if user.id not in users_id:
                course.user_set.remove(user)

        course_users_id = [user.id for user in course.user_set.all()]

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

        activity = Activity.objects.get_or_create(repo=data["repo"], user=user)[0]

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = request.user

        if not user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = request.data

        activity = get_object_or_404(Activity, id=data["id"])

        activity.grade = data["grade"]

        activity.save()

        serializer = ActivitySerializer(activity)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ActivityFilterByStudentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user

        if not user.is_staff:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            student = User.objects.get(id=user_id)

            student_activities = [
                ActivitySerializer(activity).data
                for activity in Activity.objects.filter(user=student)
            ]

            return Response(student_activities, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid user_id."}, status=status.HTTP_404_NOT_FOUND
            )
