from django.contrib.auth import authenticate, login
from rest_framework import views, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets

from accounts import models, serializers
from core.utils import get_encrypted_email


class UserViewSet(viewsets.GenericViewSet):
    """
    Used for registration and login User.
    """
    authentication_classes = ()
    model = models.User
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'email'
    lookup_url_kwarg = 'email'

    @list_route(methods=['post', ])
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.send_verification_mail()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @list_route(methods=['post', ])
    def login(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['get', ])
    def verify(self, request, *args, **kwargs):  # noqa
        hashed_email = kwargs.get(self.lookup_url_kwarg)
        self.kwargs.update(
            {self.lookup_url_kwarg: get_encrypted_email(hashed_email)}
        )
        user = self.get_object()
        user.set_verified()
        return Response(status=status.HTTP_200_OK)
