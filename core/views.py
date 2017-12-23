from django.conf import settings
from django.db import connections
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class HealthView(ViewSet):
    """
    Perform healthcheck of service
    """
    permission_classes = ()
    authentication_classes = ()

    def list(self, request):  # noqa
        data = {
            'db': None
        }
        if not settings.DATABASES:
            data['db'] = 'Not present'
        else:
            db_conn = connections['default']
            db_conn.cursor()
            data['db'] = 'Ok'
        return Response(data=data, status=status.HTTP_200_OK)
