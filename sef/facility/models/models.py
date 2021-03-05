import uuid

from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from sef.common.models import AbstractBase
from sef.user.models import User


PLATFORM = (
    ('ANDROID', 'ANDROID'),
    ('IOS', 'IOS'),
)

EXTRACT = (
    ('CALLS', 'CALLS'),
    ('MESSAGES', 'MESSAGES'),
    ('LOCATION', 'LOCATION'),
)

class Case(AbstractBase):
    """
    Contains useful information about a case
    """
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()

    _search_fields = ('title', 'description')

    def __str__(self):
        return '{}'.format(self.title)


class CaseFile(AbstractBase):
    """
    Holds information on a case and specific platform
    """
    case = models.ForeignKey(
        Case, on_delete=models.PROTECT, related_name='case_casefile')
    platform = models.CharField(
        _('platform'), max_length=30, choices=PLATFORM, blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    extract = ArrayField(
         models.CharField(
            _('extract'), max_length=30, choices=EXTRACT, blank=True, null=True))
    md5 = models.CharField(max_length=100)
    sha256 = models.CharField(max_length=100)
    sha512 = models.CharField(max_length=100)

    _search_fields = ('platform', 'file_path')

    class Meta:
        unique_together = ('case', 'platform', 'file_path', 'sha256')


class Facility(AbstractBase):
    facility_name = models.CharField(max_length=255, blank=True, null=True)
    latlong = PointField(null=True, blank=True)
    facility_type = models.CharField(max_length=255s, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    operation_status_name = models.CharField(
        max_length=255, blank=True, null=True)


class FacilityLocationDetails(AbstractBase):
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT,
        related_name='facility_facilitylocationdetails')
    address = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    place = models.TextField(blank=True, null=True)
    locality = models.TextField(blank=True, null=True)
    neighborhood = models.TextField(blank=True, null=True)
    poi = models.TextField(blank=True, null=True)
    landmark = models.TextField(blank=True, null=True)
    postcode = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    region = models.TextField(blank=True, null=True)
