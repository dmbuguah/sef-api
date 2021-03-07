"""Facility models."""
from django.db import models
from django.contrib.gis.db.models import PointField

from sef.common.models import AbstractBase


class Facility(AbstractBase):
    """Model to holde Facility details."""

    facility_id = models.UUIDField(null=True, blank=True)
    facility_name = models.CharField(max_length=255, blank=True, null=True)
    latlong = PointField(null=True, blank=True)
    facility_type = models.CharField(max_length=255, blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    operation_status_name = models.CharField(
        max_length=255, blank=True, null=True)
    keph_level = models.CharField(max_length=255, blank=True, null=True)
    county_name = models.CharField(max_length=255, blank=True, null=True)
    constituency_name = models.CharField(max_length=255, blank=True, null=True)
    ward_name = models.CharField(max_length=255, blank=True, null=True)


class FacilityLocationDetail(AbstractBase):
    """Model to hold Facility location details."""

    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT,
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
