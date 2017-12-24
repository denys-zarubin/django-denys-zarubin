from django.contrib.auth import authenticate, login
from django.http import HttpResponseForbidden
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from accounts import models, serializers
from core.utils import decode_email, encode_email


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
        Overridden default get_object, because PK is email and lookup_url_kwarg
        can't contain symbols like @,. due to RFC-1738
        """
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {
            self.lookup_field: decode_email(self.kwargs[lookup_url_kwarg])
        }
        obj = get_object_or_404(queryset, **filter_kwargs)
        return obj

    @list_route(methods=['post', ], permission_classes=())
    def register(self, request, *args, **kwargs):  # noqa
        team = request.META.get('TEAM')
        if team:
            request.data.update({"team": team})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        link = request.build_absolute_uri(
            reverse("accounts-user-verify",
                    kwargs={"email": encode_email(user.email)}))
        user.send_verification_mail(link)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @list_route(methods=['post', ], permission_classes=())
    def login(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['get', ])
    def verify(self, request, *args, **kwargs):  # noqa
        user = request.user
        user.set_verified()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post', ], url_path='reset')
    def reset_password(self, request, *args, **kwargs):  # noqa
        user = request.user
        user.reset_password()
        return Response(status=status.HTTP_200_OK)

    @detail_route(methods=['post', ], url_path='password')
    def set_password(self, request, *args, **kwargs):  # noqa
        """
        Set new password for user
        """
        password = request.data.get('password')
        user = request.user
        user.set_password(password)
        user.save(update_fields=['password'])
        return Response(status=status.HTTP_200_OK)


class TeamViewSet(CreateModelMixin, GenericViewSet):
    """
    Used for creating teams and inviting User to team
    """

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

    @list_route(
        methods=['get', ], url_path='assigned', permission_classes=())
    def assigned_to_team(self, request):
        """
        :param request: Request object
        :return: Redirect to form
        """
        team = request.query_params.get('team')
        # TODO: Change redirect to page with register form
        return Response(headers={"team": team}, status=status.HTTP_302_FOUND)

    @list_route(methods=['post', ])
    def send_invite(self, request):
        user = request.user
        link = request.build_absolute_uri(
            reverse('accounts-team-assigned', args=(user.team.id,)))
        user.send_invite_to_team(link)
        return Response(status=status.HTTP_200_OK)
