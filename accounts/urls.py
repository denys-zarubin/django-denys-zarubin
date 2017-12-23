from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet, TeamViewSet

router = DefaultRouter()
router.register('team', TeamViewSet, base_name='accounts-team')
router.register('', UserViewSet, base_name='accounts-user')
