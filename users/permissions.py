from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework import status


class CoursePermission(BasePermission):
    message = Response(
        {"detail": "You do not have permission to perform this action."},
        status=status.HTTP_403_FORBIDDEN,
    )

    def has_permission(self, request, view):
        if request.method == "GET":
            return True

        superuser = request.user.is_superuser

        staff = request.user.is_staff

        if superuser and staff:
            return True
