from django.urls import path
from users.views import UserView

urlpatterns = [
    path("accounts/", UserView.as_view()),
]
