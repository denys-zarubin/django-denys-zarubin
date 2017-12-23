from django.conf import settings
from django.conf.urls import include, url
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from core.views import HealthView

router = DefaultRouter(trailing_slash=True)
router.register('health', HealthView, base_name='health_check')

urlpatterns = [
    url(r'', include(router.urls)),
]
if settings.DEBUG:
    # For local development
    from django.views.static import serve

    urlpatterns = [url(r'^docs/', include_docs_urls(title='Api')),
                   url(r'^static/(?P<path>.*)$', serve, {
                       'document_root': settings.STATIC_ROOT,
                   }), ] + urlpatterns
