"""Facility app urls."""
from rest_framework.routers import SimpleRouter

import sef.facility.views as views

router = SimpleRouter()
router.register(r'facilities', views.FacilityViewSet, 'facilities')
router.register(
    r'facility_location_details', views.FacilityLocationDetailViewSet,
    'facility_location_details')

urlpatterns = router.urls
