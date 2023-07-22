from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response

from documentio.common.serializers import UserSlimSerializer
from documentio.models import User

from ..serializers.users import PublicUserRegisterSerializer, PublicUserLoginSerializer


class PublicUserRegistration(CreateAPIView):
    serializer_class = PublicUserRegisterSerializer


class PublicUserLogin(CreateAPIView):
    serializer_class = PublicUserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = super().create(request, *args, **kwargs)
        return Response(status=status.HTTP_200_OK, data=data.data)


class PublicUserList(ListAPIView):
    queryset = User.objects.filter()
    serializer_class = UserSlimSerializer
