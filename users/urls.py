from django.urls import path
from users.views import (
    UserView,
    CourseView,
    ActivityView,
    ActivityFilterByStudentView,
)

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("courses/", CourseView.as_view()),
    path("activities/", ActivityView.as_view()),
    path("activities/<int:user_id>", ActivityFilterByStudentView.as_view()),
]
