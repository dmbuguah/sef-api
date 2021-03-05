import datetime
import requests
import subprocess
import xml.etree.ElementTree as ET

from dateutil.parser import parse
from django.conf import settings
from django.contrib.gis.geos import fromstr

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import list_route

from sef.constants import (
    SMS_XML_PATH, METADATA_XML_PATH, CREATOR_XML_PATH, RUSAGE_XML_PATH,
    RUSAGE_NS, SMS_NS, CALL_XML_PATH, CALL_NS, LOCATION_XML_PATH,
    LOCATION_NS)
from sef.common.views import NuggetBaseViewSet
from sef.case import filters
from sef.case import serializers
from sef.case import models
from sef.case.utils import (
    extract_resorce, get_platform, generate_nugget_dsl, get_extracts)
from sef.case.analytics.analysis import (
    get_out_going_calls_by_day, get_calls_by_ctype_date,
    get_sms_by_date_sent, get_sms_by_date_received, get_sms_by_type_date,
    get_case_location, get_dashboard_infor, get_location_timeline,
    get_all_received_sms, get_all_sent_sms, get_incoming_calls_by_day,
    get_case_count)
from sef.case.tasks.utils import geocode_reverse

from sef.case.analytics.calls import (
    get_incoming_calls_by_contact, _get_conversation_timeline)

from rest_framework.response import Response
from rest_framework.decorators import list_route


class CaseViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Case.objects.all()
    filter_class = filters.CaseFilter
    serializer_class = serializers.CaseSerializer

    def create_call(self, call_root, case):
        call_list = []
        for call in call_root:
            cfrom = extract_resorce(call, 'from:from', CALL_NS)
            cdate_called = extract_resorce(call, 'date_called:date_called', CALL_NS)
            country_code = extract_resorce(call, 'country_code:country_code', CALL_NS)
            ctype = extract_resorce(call, 'type:type', CALL_NS)
            duration = extract_resorce(call, 'duration:duration', CALL_NS)
            call_obj = {
                'case': case,
                'cfrom': cfrom,
                'cduration': duration,
                'date_called': cdate_called,
                'country_code': country_code,
                'ctype': ctype,
            }
            call_list.append(call_obj)

        if call_list:
            models.CallLog.objects.bulk_create(
                [ models.CallLog(**c) for c in call_list ])
        return call_list

    def create_msg(self, sms_mms_root, case):
        msg_list = []
        for sms in sms_mms_root:
            kind = extract_resorce(sms, 'kind:kind', SMS_NS)
            body = extract_resorce(sms, 'body:body', SMS_NS)
            recipient = extract_resorce(sms, 'recipient:recipient', SMS_NS)
            date_sent = extract_resorce(sms, 'date_sent:date_sent', SMS_NS)
            sender = extract_resorce(sms, 'sender:sender', SMS_NS)
            date_received = extract_resorce(
                sms, 'date_received:date_received', SMS_NS)
            country_code = extract_resorce(
            sms, 'country_code:country_code', SMS_NS)
            read = extract_resorce(sms, 'read:read', SMS_NS)
            type = extract_resorce(sms, 'type:type', SMS_NS)

            msg_obj = {
                'case': case,
                'kind': kind,
                'body': body,
                'recipient': recipient,
                'date_sent': date_sent,
                'read': read,
                'type': type,
                'sender': sender,
                'date_received': date_received,
                'country_code': country_code
            }
            msg_list.append(msg_obj)

        if msg_list:
            models.Message.objects.bulk_create(
                [ models.Message(**m) for m in msg_list ])
        return msg_list

    def create_location(self, location_root, case):
        location_list = []
        for location in location_root:
            long = extract_resorce(location, 'long:long', LOCATION_NS)
            lat = extract_resorce(location, 'lat:lat', LOCATION_NS)
            source = extract_resorce(location, 'source:source', LOCATION_NS)
            confidence = extract_resorce(location, 'confidence:confidence', LOCATION_NS)
            timestamp = extract_resorce(location, 'timestamp:timestamp', LOCATION_NS)
            wifi_mac = extract_resorce(location, 'wifi_mac:wifi_mac', LOCATION_NS)
            latlong = fromstr(f'POINT({float(long)} {float(lat)})', srid=4326)
            location_obj = {
                'case': case,
                'latlong': latlong,
                'source': source,
                'confidence': confidence,
                'timestamp': timestamp,
                'wifi_mac': wifi_mac
            }
            location_list.append(location_obj)

        if location_list:
            models.Location.objects.bulk_create(
                [ models.Location(**l) for l in location_list ])
        return location_list

    def create_rusage(self, rusage_root, case):
        utime = extract_resorce(rusage_root, 'utime:utime', RUSAGE_NS)
        stime = extract_resorce(rusage_root, 'stime:stime', RUSAGE_NS)
        maxrss = extract_resorce(rusage_root, 'maxrss:maxrss', RUSAGE_NS)
        minflt = extract_resorce(rusage_root, 'minflt:minflt', RUSAGE_NS)
        majflt = extract_resorce(rusage_root, 'majflt:majflt', RUSAGE_NS)
        nswap = extract_resorce(rusage_root, 'nswap:nswap', RUSAGE_NS)
        inblock = extract_resorce(rusage_root, 'inblock:inblock', RUSAGE_NS)
        oublock = extract_resorce(rusage_root, 'oublock:oublock', RUSAGE_NS)
        clocktime = extract_resorce(
            rusage_root, 'clocktime:clocktime', RUSAGE_NS)

        rusage_obj = {
            'case': case,
            'utime': utime,
            'stime': stime,
            'maxrss': maxrss,
            'minflt': minflt,
            'majflt': majflt,
            'nswap': nswap,
            'inblock': inblock,
            'oublock': oublock,
            'clocktime': clocktime
        }
        return rusage_obj


    def get_process_info(self, platform, file_path, extract):
        nugget_dsl_file_path = generate_nugget_dsl(platform, file_path, extract)
        process = subprocess.Popen(
            ['go', 'run', 'github.com/cdstelly/nugget', '-input',
            nugget_dsl_file_path], stderr=subprocess.PIPE,
            stdout=subprocess.PIPE, cwd=settings.WORKING_DIR)
        out, err = process.communicate()
        print(out)
        return out, err


    def get_root_nodes(self, decoded_op):
        decoded_op = decoded_op.decode("utf-8")
        raw_decoded_op = decoded_op.split('as dfxml\n', 1)[-1]
        root = ET.fromstring(raw_decoded_op)

        call_root = root.findall(CALL_XML_PATH)
        sms_mms_root = root.findall(SMS_XML_PATH)
        rusage_root = root.find(RUSAGE_XML_PATH)
        location_root = root.findall(LOCATION_XML_PATH)

        return call_root, sms_mms_root, rusage_root, location_root

    def create_case_file(self, **case_file):
        case_file = models.CaseFile.objects.create(**case_file)
        return case_file

    @list_route(methods=('get',))
    def get_all_cases(self, request):

        res = get_case_count()
        _response = {
            'case_stats': res
        }
        return Response(_response)

    @list_route(methods=('get',))
    def case_analysis(self, request):
        case_id =  self.request.query_params['caseId']
        case = models.Case.objects.get(id=case_id)

        outgoing_calls_by_day = get_out_going_calls_by_day(case)
        incoming_calls_by_day = get_incoming_calls_by_day(case)

        calls_by_ctype = get_calls_by_ctype_date(case)

        sms_sent_by_day = get_sms_by_date_sent(case)
        sms_received_by_day = get_sms_by_date_received(case)
        sms_by_type_date = get_sms_by_type_date(case)
        location_case = get_case_location(case)
        sms, calls, location = get_dashboard_infor(case)

        conversation_timeline = _get_conversation_timeline(case)

        _response = {
            'dashboard': {
                'sms': sms,
                'call': calls,
                'location': location
            },
            'outgoing_calls_by_day': {
                'title': 'Outgoing call count by day analysis',
                'analysis_data': outgoing_calls_by_day
            },
            'incoming_calls_by_day': {
                'title': 'Incoming call count by day analysis',
                'analysis_data': incoming_calls_by_day
            },
            'sms_sent_by_day': {
                'title': 'SMS sent by day analysis',
                'analysis_data': sms_sent_by_day
            },
            'sms_received_by_day': {
                'title': 'SMS received by day analysis',
                'analysis_data': sms_received_by_day
            },
            'calls_by_ctype': {
                'title': 'Incoming call count by contact person',
                'analysis_data': calls_by_ctype
            },
            'sms_by_type_date': {
                'title': 'SMS count by date and category',
                'analysis_data': sms_by_type_date
            },
            'location_case': {
                'title': 'User location data',
                'analysis_data': location_case
            },
            'conversation_timeline': {
                'title': 'Conversation TimeLine',
                'analysis_data': conversation_timeline
            }
        }
        return Response(_response)


    @list_route(methods=('get',))
    def get_incoming_calls(self, request):
        date_called = self.request.query_params['dateCalled']
        case_id = self.request.query_params['caseId']
        case = models.Case.objects.get(id=case_id)

        _all_incoming_calls = get_incoming_calls_by_contact(case, date_called)
        _response = {
            'incoming_calls': {
                'title': 'Incoming calls by contact person',
                'analysis_data': _all_incoming_calls
            }
        }

        return Response(_response)


    @list_route(methods=('get',))
    def get_received_sms(self, request):
        date_received = self.request.query_params['dateReceived']
        case_id = self.request.query_params['caseId']
        case = models.Case.objects.get(id=case_id)

        _all_received_sms = get_all_received_sms(case, date_received)
        _response = {
            'received_sms': {
                'title': 'Received sms breakdown by contact person',
                'analysis_data': _all_received_sms
            }
        }

        return Response(_response)


    @list_route(methods=('get',))
    def get_sent_sms(self, request):
        date_sent = self.request.query_params['dateSent']
        case_id = self.request.query_params['caseId']
        case = models.Case.objects.get(id=case_id)

        _all_sent_sms = get_all_sent_sms(case, date_sent)
        _response = {
            'sent_sms': {
                'title': 'Sent sms breakdown by contact person',
                'analysis_data': _all_sent_sms
            }
        }

        return Response(_response)

    @list_route(methods=('get',))
    def marker_analysis(self, request):
        location_id = self.request.query_params['locationId']
        x_minutes = self.request.query_params.get('xMinutes')
        case_id = self.request.query_params['caseId']

        location = models.Location.objects.get(id=location_id)

        loc_time = location.timestamp
        loc_upper_bound = loc_time + datetime.timedelta(minutes=20)
        loc_lower_bound = loc_time - datetime.timedelta(minutes=20)

        location_timeline = get_location_timeline(
            case_id, location_id, loc_upper_bound, loc_lower_bound)

        _response = {
            'location_timeline': {
                'title': 'User location data',
                'analysis_data': location_timeline
            }
        }
        return Response(_response)

    @list_route(methods=('get',))
    def location_analysis(self, request):
        case_id = self.request.query_params['caseId']
        date_from = self.request.query_params['dateFrom']
        date_to = self.request.query_params['dateTo']

        date_from = parse(date_from).date()
        date_to = parse(date_to).date()

        case = models.Case.objects.get(id=case_id)
        location_case = get_case_location(case, date_from, date_to)

        _response = {
            'location_case': {
                'title': 'User location data',
                'analysis_data': location_case
            }
        }
        return Response(_response)

    @list_route(methods=('post',))
    def create_case(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        platform = request.data.get('platform')

        case_data = {
            'title': title,
            'description': description
        }
        case = models.Case.objects.create(**case_data)

        platform = request.data.get('platform')
        file_path = request.data.get('file_path')
        extract = request.data.get('extract')
        case_file = {
            'case':  case,
            'platform': platform,
            'file_path': file_path,
            'extract': extract
        }
        case_file = self.create_case_file(**case_file)
        platform = get_platform(platform)
        decoded_extracts = get_extracts(extract)

        for ext in decoded_extracts:
            import pdb; pdb.set_trace()
            process_info, err = self.get_process_info(platform, file_path, ext)
            call_root, sms_mms_root, rusage_root, location_root = \
                self.get_root_nodes(process_info)
            rusage_obj = self.create_rusage(rusage_root, case)
            processed_call = self.create_call(call_root, case)
            processed_msg = self.create_msg(sms_mms_root, case)
            processed_location = self.create_location(location_root, case)
        geocode_reverse(case=case)
        return Response()


class CaseFileViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.CaseFile.objects.all()
    filter_class = filters.CaseFileFilter
    serializer_class = serializers.CaseFileSerializer


class LocationViewSet(NuggetBaseViewSet):
    """
    This provides a way to add Case details.
    """
    permission_classes = (AllowAny, )
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
