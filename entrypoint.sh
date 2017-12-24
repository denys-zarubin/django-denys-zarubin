#!/bin/sh

cd /django/

# Collect static Files
echo "Collect static Files"
python manage.py collectstatic -v 0 --noinput --settings=core.settings.base

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate -v 1

# Start server
echo "Starting server"
uwsgi --http 0.0.0.0:8000 \
      --master \
      --module "core.wsgi:get_wsgi_application()" \
      --static-map /static=/static \
      --py-autoreload 1
