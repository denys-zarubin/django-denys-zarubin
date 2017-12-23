#!/bin/sh

cd /django/core/
# Apply database migrations
echo "Apply database migrations"
python manage.py migrate -v 1

# Start server
echo "Starting server"
uwsgi --http 0.0.0.0:8000 \
      --master \
      --module "django.core.wsgi:get_wsgi_application()" \
      --disable-logging \
      --static-map /static=/static \
      $EXTRA

