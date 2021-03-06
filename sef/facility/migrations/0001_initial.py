# Generated by Django 2.0.4 on 2021-03-06 09:47

import django.contrib.gis.db.models.fields
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('ts_document', models.TextField(blank=True, help_text='The content that will be searched over', null=True)),
                ('ts_document_vector', django.contrib.postgres.search.SearchVectorField(blank=True, help_text='The ts_vector for the document field', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('facility_id', models.UUIDField(blank=True, null=True)),
                ('facility_name', models.CharField(blank=True, max_length=255, null=True)),
                ('latlong', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('facility_type', models.CharField(blank=True, max_length=255, null=True)),
                ('owner_name', models.CharField(blank=True, max_length=255, null=True)),
                ('operation_status_name', models.CharField(blank=True, max_length=255, null=True)),
                ('keph_level', models.CharField(blank=True, max_length=255, null=True)),
                ('county_name', models.CharField(blank=True, max_length=255, null=True)),
                ('constituency_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ward_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilityLocationDetail',
            fields=[
                ('ts_document', models.TextField(blank=True, help_text='The content that will be searched over', null=True)),
                ('ts_document_vector', django.contrib.postgres.search.SearchVectorField(blank=True, help_text='The ts_vector for the document field', null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('address', models.TextField(blank=True, null=True)),
                ('country', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('locality', models.TextField(blank=True, null=True)),
                ('neighborhood', models.TextField(blank=True, null=True)),
                ('poi', models.TextField(blank=True, null=True)),
                ('landmark', models.TextField(blank=True, null=True)),
                ('postcode', models.TextField(blank=True, null=True)),
                ('district', models.TextField(blank=True, null=True)),
                ('region', models.TextField(blank=True, null=True)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='facility_facilitylocationdetails', to='facility.Facility')),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'abstract': False,
            },
        ),
    ]
