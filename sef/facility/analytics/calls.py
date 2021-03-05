import datetime

from django.db.models import Count
from itertools import chain
from django.db import connection

from sef.case.models import CallLog, Message, Location

def get_incoming_calls_by_contact(case, date_called):
        """[
            {
                'user': '+23183773',
                'call': [
                    {
                        'country_code': '310',
                        'date_called': '2012-08-02',
                        'cduration': '20'
                    },
                    {
                        'country_code': '310',
                        'date_called': '2012-08-02',
                        'cduration': '20'
                    }
                ]
            },
            {
                'user': '+23183773',
                'call': [
                    {
                        'country_code': '310',
                        'date_called': '2012-08-02',
                        'cduration': '20'
                    },
                    {
                        'country_code': '310',
                        'date_called': '2012-08-02',
                        'cduration': '20'
                    }
                ]
            }
        ]"""
        incoming_calls = CallLog.objects.filter(
            case=case, date_called__date=date_called,
            ctype='incoming').values_list('cfrom', flat=True)

        all_unique_users = list(set(list(incoming_calls)))
        _all_incoming_calls = []
        for all_unique_user in all_unique_users:
            single_user_call = {}
            _cfrom = all_unique_user
            all_sms = CallLog.objects.filter(
                case=case, date_called__date=date_called,
                cfrom=all_unique_user).values(
                'country_code', 'date_called', 'cduration')
            single_user_call = {
                'user': _cfrom,
                'call': list(all_sms)
            }
            _all_incoming_calls.append(single_user_call)

        return _all_incoming_calls


def _get_conversation_timeline(case):
    """[
            {
                'user': '+17038296071',
                'conv': [
                    {
                        'date_time': '2012-08-02',
                        'type': 'sent',
                        'body': 'Message body'
                    },
                    {
                        'date_time': '2012-08-02',
                        'type': 'received',
                        'body': 'Message body'
                    }
                ]
            }
    ]"""
    sent_sms = Message.objects.filter(
        case=case, recipient__isnull=False).values_list('recipient', flat=True)
    received_sms = Message.objects.filter(
        case=case, sender__isnull=False).values_list('sender', flat=True)
    received_calls = CallLog.objects.filter(
        case=case, cfrom__isnull=False).values_list('cfrom', flat=True)
    case_location = Location.objects.filter(case=case)
    received_calls = ['+1' + x for x in received_calls]

    sent_sms = list(set(list(sent_sms)))
    received_sms = list(set(list(received_sms)))
    all_sms_contacts = list(set([*sent_sms, *received_sms, *received_calls]))

    all_conv_persons = []
    for all_sms_contact in all_sms_contacts:
        single_conv_obj = {}
        received_sms = Message.objects.filter(
            case=case, sender=all_sms_contact).values(
                'type', 'date_received', 'body')
        sent_sms = Message.objects.filter(
            case=case, recipient=all_sms_contact).values(
            'type', 'date_sent', 'body')
        incoming_calls = CallLog.objects.filter(
            case=case, cfrom=all_sms_contact.strip('+1')).values(
                'ctype', 'cduration', 'date_called')
        incoming_calls = [{
            'cduration': x['cduration'],
            'type': x['ctype'],
            'body': 'Call received from {}'.format(all_sms_contact),
            'date': x.get('date_called')
        } for x in incoming_calls]

        _cov_list =  list(received_sms) + list(sent_sms) + list(incoming_calls)
        conv_list = []

        for x in _cov_list:
            _date = x.get('date_received', x.get('date_sent', x.get('date')))
            loc_upper_bound = _date + datetime.timedelta(minutes=40)
            loc_lower_bound = _date - datetime.timedelta(minutes=40)

            _case_loc = case_location.filter(
                timestamp__lte=loc_upper_bound,
                timestamp__gte=loc_lower_bound)
            if _case_loc:
                _case_loc = _case_loc[0]
                _location_details = _case_loc.location_locationdetails.all()
                if _location_details:
                    _location_details = _location_details[0].place
            else:
                _location_details = None

            conv_dict = {
                'body': x.get('body'),
                'ctype': x.get('ctype'),
                'type': x.get('type') or 'inbox',
                'cduration': x.get('cduration'),
                'date': _date,
                '_location': _location_details
            }
            conv_list.append(conv_dict)

        sorted_conv = sorted(conv_list, key=lambda x: x['date'], reverse=False)

        single_conv_obj = {
            'user': all_sms_contact,
            'conv': sorted_conv
        }
        all_conv_persons.append(single_conv_obj)

    return all_conv_persons
