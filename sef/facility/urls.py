from rest_framework.routers import SimpleRouter

import sef.case.views as views

router = SimpleRouter()
router.register(r'cases', views.CaseViewSet, 'cases')
router.register(r'case_files', views.CaseFileViewSet, 'case_files')
router.register(r'location', views.LocationViewSet, 'location')

urlpatterns = router.urls
