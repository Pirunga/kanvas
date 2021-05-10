from django.urls import path
from authentication.views import LoginView


urlapatterns = [
    path("login/", LoginView.as_view()),
]
