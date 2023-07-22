from django.urls import path

from ..views.users import PublicUserRegistration, PublicUserLogin, PublicUserList

urlpatterns = [
    path("", PublicUserList.as_view(), name="user.list"),
    path("login/", PublicUserLogin.as_view(), name="user.login"),
    path("register/", PublicUserRegistration.as_view(), name="user.register"),
]
