from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, base_name='accounts-user')
