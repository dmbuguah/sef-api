from rest_framework.routers import SimpleRouter

import sef.user.views as views

router = SimpleRouter()
router.register(r'users', views.UserViewSet, 'users')

urlpatterns = router.urls
