from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponseNotAllowed, HttpResponseForbidden
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet

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

    def get_object(self):
        """
        Overriden default one, because email with @ or . can be as part of url,
        RFC-1738
        """
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: get_encrypted_email(self.kwargs[lookup_url_kwarg])
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

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
        user = self.get_object()
        user.set_verified()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post', ], url_path='reset')
    def reset_password(self, request, email):  # noqa
        user = self.get_object()
        user.reset_password()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post', ], url_path='password')
    def set_password(self, request, email):  # noqa
        password = request.data.get('password')
        user = self.get_object()
        user.set_password(password)
        user.save(update_fields=['password'])
        return Response(status=status.HTTP_200_OK)


class TeamViewSet(CreateModelMixin, GenericViewSet):
    """
    Used for creating teams and inviting User to team
    """
    # authentication_classes = ()
    model = models.Team
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.team:
            return HttpResponseForbidden(
                content='You should be not part of team'
            )

        instance = serializer.save()
        user.team = instance
        user.save()
