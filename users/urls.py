from django.urls import path
from users.views import (
    UserView,
    CourseView,
    ActivityView,
)

urlpatterns = [
    path("accounts/", UserView.as_view()),
    path("courses/", CourseView.as_view()),
    path("activities/", ActivityView.as_view()),
]
