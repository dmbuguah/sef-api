import uuid

from django.db import models
from django.utils import timezone

from sef.pg_search.mixins import SearchModelMixin


class AbstractBase(SearchModelMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ('-updated', '-created',)
