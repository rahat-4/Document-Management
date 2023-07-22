from django.urls import path, include

urlpatterns = [
    path("users/", include("documentio.rest.urls.users")),
    path("documents/", include("documentio.rest.urls.documents"))
]