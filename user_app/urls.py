from rest_framework import routers

from user_app.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'', UserViewSet)
