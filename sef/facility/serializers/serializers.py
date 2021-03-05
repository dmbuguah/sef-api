from rest_framework import serializers

import sef.case.models as models


class CaseFileSerializerReadOnly(serializers.ModelSerializer):
    platform = serializers.ReadOnlyField()
    file_path = serializers.ReadOnlyField()
    extract = serializers.ReadOnlyField()
    md5 = serializers.ReadOnlyField()
    sha256 = serializers.ReadOnlyField()
    sha512 = serializers.ReadOnlyField()

    class Meta:
        model = models.CaseFile
        fields = (
        'id', 'platform', 'file_path', 'extract', 'md5', 'sha256', 'sha512')


class CaseFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CaseFile
        fields = (
            'id', 'platform', 'file_path', 'extract', 'md5', 'sha256', 'sha512')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = (
            'id', 'case', 'confidence', 'timestamp', 'wifi_mac')


class CaseSerializer(serializers.ModelSerializer):
    case_file = CaseFileSerializerReadOnly(
        source = 'case_casefile', read_only=True, required=False, many=True,)
    extracts = serializers.SerializerMethodField()
    platforms = serializers.SerializerMethodField()

    def get_extracts(self, instance):
        cfs = instance.case_casefile.all()
        all_extracts = [cf.extract for cf in cfs]

        if all_extracts:
            all_extracts = all_extracts[0]
            return " , ".join(v for v in all_extracts)
        else:
            return None

    def get_platforms(self, instance):
        cfs = instance.case_casefile.all()
        all_platforms = [cf.platform for cf in cfs]

        if all_platforms:
            return " , ".join(v for v in all_platforms)
        else:
            return None

    class Meta:
        model = models.Case
        fields = (
            'id', 'title', 'description', 'case_file', 'extracts', 'platforms')
