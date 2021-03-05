"""Analysis module."""
import datetime

from django.db.models import Count
from itertools import chain
from django.db import connection

from sef.case.models import CallLog, Message, Location, CaseFile


def get_specific_location_by_date(scc):
    q_sms = scc.filter().extra(
        select={'_timestamp': 'DATE(timestamp)'}).values(
            '_timestamp').annotate(call_count=Count('case')).order_by()
    return q_sms

def get_specific_sms_by_date_received(scc):
    # analysed
    q_sms = scc.filter(type__isnull=False, date_received__isnull=False).extra(
        select={'_date_received': 'DATE(date_received)'}).values(
            '_date_received').annotate(sms_count=Count('case')).order_by()
    return q_sms

def get_specific_sms_by_date_sent(scc):
    # analysed
    q_sms = scc.filter(type__isnull=False, date_sent__isnull=False).extra(
          select={'_comm_date': 'DATE(date_sent)'}).values(
              '_comm_date').annotate(sms_count=Count('case')).order_by()
    return q_sms


def get_specific_calls_by_date(scc):
    # analysed
    q_calls = scc.extra(select={'_date_called': 'DATE(date_called)'}).values(
            '_date_called').annotate(call_count=Count('case')).order_by()
    return q_calls

def get_out_going_specific_calls_by_date(scc):
    # analysed
    q_calls = scc.filter(ctype='outgoing').extra(
        select={'_date_called': 'DATE(date_called)'}).values(
            '_date_called').annotate(call_count=Count('case')).order_by()
    return q_calls


def get_incoming_specific_calls_by_date(scc):
    # analysed
    q_calls = scc.filter(ctype='incoming').extra(
        select={'_date_called': 'DATE(date_called)'}).values(
            '_date_called').annotate(call_count=Count('case')).order_by()
    return q_calls


def get_out_going_calls_by_day(case):
    # analysed
    """Get specific case calls by day.

    Given a case, get call logs grouped by the day the calls were made.
    Returns data if the format below:

    [
        {
            'call_count': 2, '_date_called': datetime.date(2012, 6, 12)
        },
        {
            'call_count': 1, '_date_called': datetime.date(2012, 6, 13)
        }
    ]

    """
    specific_case_calls = CallLog.objects.filter(case=case)
    q_calls = get_out_going_specific_calls_by_date(specific_case_calls)
    return q_calls


def get_incoming_calls_by_day(case):
    # analysed
    """Get specific case calls by day.

    Given a case, get call logs grouped by the day the calls were made.
    Returns data if the format below:

    [
        {
            'call_count': 2, '_date_called': datetime.date(2012, 6, 12)
        },
        {
            'call_count': 1, '_date_called': datetime.date(2012, 6, 13)
        }
    ]

    """
    specific_case_calls = CallLog.objects.filter(case=case)
    q_calls = get_incoming_specific_calls_by_date(specific_case_calls)
    return q_calls


def get_calls_by_ctype_date(case):
    # analysed
    """Get specific case calls by ctype.

    The response is a list of ctypes by date as below
    [
        {
            '_call_date': datetime.date(2012, 6, 12), 'incoming': 4
        },
        {
            '_call_date': datetime.date(2012, 6, 13), 'outgoing': 2
        }
    ]
    """
    specific_case_calls = CallLog.objects.filter(case=case)

    q_calls = get_specific_calls_by_date(specific_case_calls)
    unique_dates_list =  [c['_date_called'] for c in q_calls]

    calls_by_ctype = {}
    calls_by_ctype_list = []
    for _date in unique_dates_list:
        calls_by_ctype = {}
        ctype_by_count = specific_case_calls.filter(
            date_called__date=_date).values(
            'ctype').annotate(ctype_count=Count('ctype')).order_by()
        calls_by_ctype['_call_date'] = _date
        calls_by_ctype.update(
            [{x['ctype']: x['ctype_count']} for x in ctype_by_count][0])
        calls_by_ctype_list.append(calls_by_ctype)

    return calls_by_ctype_list


def get_sms_by_type_date(case):
    # analysed
    """Get specific case sms by type and date.

    The response is a list of sms by date and type as below
    [
        {
            '_sms_date': datetime.date(2012, 7, 11), 'inbox': 1, 'sent': 1
        },
        {
            '_sms_date': datetime.date(2012, 7, 10), 'inbox': 2, 'outbox': 1
        }
    ]
    """
    specific_case_msg = Message.objects.filter(case=case)

    received_dates = specific_case_msg.filter(
        type__isnull=False).values_list('date_received', flat=True)
    _received_dates = list(set([x.date() for x in received_dates if x]))

    sent_dates = specific_case_msg.filter(
        type__isnull=False).values_list('date_sent', flat=True)
    _sent_dates = list(set([x.date() for x in sent_dates if x]))
    _all_dates = list(set(_received_dates) | set(_sent_dates))

    sms_by_type_list = []
    sms_by_type = {}
    _first_round = 0
    for _date in _all_dates:
        _na = False
        _first_round += 1
        sms_by_type = {}
        type_by_count_v1 = specific_case_msg.filter(
            date_received__date=_date).values(
                'type').annotate(type_count=Count('type')).order_by()
        type_by_count_v2 = specific_case_msg.filter(
            date_sent__date=_date).values(
                'type').annotate(type_count=Count('type')).order_by()
        sms_by_type['_sms_date'] = _date

        _type_by_count_v1 = [{x['type']: x['type_count']} for x in type_by_count_v1]
        _type_by_count_v2 = [{x['type']: x['type_count']} for x in type_by_count_v2]
        if _type_by_count_v1:
            for _type_by_count_v11 in _type_by_count_v1:
                sms_by_type.update(_type_by_count_v11)

        if _type_by_count_v2:
            for _type_by_count_v22 in _type_by_count_v2:
                sms_by_type.update(_type_by_count_v22)

        if _first_round == 1:
            sms_by_type_list.append(sms_by_type)
        else:
            for _sms_d in sms_by_type_list:
                if _sms_d['_sms_date'] != _date:
                    _na = True
                else:
                    _na = False
        if _na:
            sms_by_type_list.append(sms_by_type)

    return sms_by_type_list


def get_sms_by_date_sent(case):
    # analysed
    """Get specific case sms by date sent."""
    specific_sent_case_sms = Message.objects.filter(case=case)
    q_sms = get_specific_sms_by_date_sent(specific_sent_case_sms)

    q_sms = [s for s in q_sms]
    return q_sms


def get_sms_by_date_received(case):
    # analysed
    """Get specific case sms by date received."""
    specific_sent_case_sms = Message.objects.filter(case=case)
    q_sms = get_specific_sms_by_date_received(specific_sent_case_sms)

    q_sms = [s for s in q_sms]
    return q_sms


def get_sms_sent_by_date_sent_recipient(case):
    """Get sms by date sent and recipient.

    We aggregate all sent sms to find out the date they were sent, to whome,
    how many times, and what specific times. The format of the response is
    as below.

    [
        {
            datetime.date(2012, 6, 13): [
                {
                    'recipient': '+15713083236',
                    'sent_count': 1,
                    'sent_dates': [datetime.datetime(2012, 6, 13, 18, 30, 38, tzinfo=<UTC>)]},
                {
                    'recipient': '+17038296071',
                    'sent_count': 1,
                    'sent_dates': [datetime.datetime(2012, 6, 13, 18, 33, 46, tzinfo=<UTC>)]
                }
            ],
            datetime.date(2012, 7, 6): [
                {
                    'recipient': '+12027252124',
                    'sent_count': 1,
                    'sent_dates': [datetime.datetime(2012, 7, 6, 16, 27, 50, tzinfo=<UTC>)]},
                {
                    'recipient': '+15713083236',
                    'sent_count': 2,
                    'sent_dates': [datetime.datetime(2012, 7, 6, 15, 11, 54, tzinfo=<UTC>),
                    datetime.datetime(2012, 7, 6, 15, 2, 19, tzinfo=<UTC>)]}],
                }
            ]
        }
    ]
    """
    q_sms = get_specific_sms_by_date_sent(case)
    unique_date_sent = [s['_date_sent'] for s in q_sms]

    sms_by_recipient = {}
    sms_by_recipient_list = []
    for _date in unique_date_sent:
        sent_count = Message.objects.filter(
            date_sent__date=_date).values(
                'recipient').annotate(sent_count=Count('recipient')).order_by()
        sent_list = [ct for ct in sent_count]

        for s in sent_list:
            recipient_sent_date = Message.objects.filter(
                date_sent__date=_date, recipient=s['recipient']).values_list(
                'date_sent', flat=True)
            s['sent_dates'] = list(recipient_sent_date)

        sms_by_recipient[_date] = sent_list
    sms_by_recipient_list.append(sms_by_recipient)

    return sms_by_recipient_list


def get_sms_sent_by_date_received_recipient(case):
    """Get sms by date received and recipient.

    We aggregate all received sms to find out the date they were received,
    from who, how many times, and what specific times. The format of the
    response is as below.

    [
        {
            datetime.date(2012, 6, 13): [
                {
                    'sender': '+15713083236',
                    'received_count': 1,
                    'date_received': [datetime.datetime(2012, 6, 13, 18, 30, 38, tzinfo=<UTC>)]},
                {
                    'sender': '+17038296071',
                    'received_count': 1,
                    'date_received': [datetime.datetime(2012, 6, 13, 18, 33, 46, tzinfo=<UTC>)]
                }
            ],
            datetime.date(2012, 7, 6): [
                {
                    'sender': '+12027252124',
                    'received_count': 1,
                    'date_received': [datetime.datetime(2012, 7, 6, 16, 27, 50, tzinfo=<UTC>)]},
                {
                    'sender': '+15713083236',
                    'received_count': 2,
                    'date_received': [datetime.datetime(2012, 7, 6, 15, 11, 54, tzinfo=<UTC>),
                    datetime.datetime(2012, 7, 6, 15, 2, 19, tzinfo=<UTC>)]}],
                }
            ]
        }
    ]
    """
    a_sms = Message.objects.filter(case=case)

    q_sms = get_specific_sms_by_date_received(a_sms)
    unique_date_received = [s['_date_received'] for s in q_sms]

    sms_by_sender = {}
    sms_by_sender_list = []
    for _date in unique_date_received:
        received_count = Message.objects.filter(
            date_received__date=_date).values(
                'sender').annotate(received_count=Count('sender')).order_by()
        received_list = [ct for ct in received_count]

        for s in received_list:
            sender_received_date = Message.objects.filter(
                date_received__date=_date, sender=s['sender']).values_list(
                'date_received', flat=True)
            s['date_received'] = list(sender_received_date)

        sms_by_sender[_date] = received_list
    sms_by_sender_list.append(sms_by_sender)

    return sms_by_recipient_list


def get_case_location_by_date(case):
    """Get case location."""
    q_location = get_specific_location_by_date(case)
    unique_timestamp = [l['_timestamp'] for l in q_location]

    location_date = {}
    location_date_list = []
    for _date in unique_timestamp:
        location_by_date = Location.objects.filter(
            timestamp__date=_date, case=case).order_by('timestamp'
            ).values('latlong', 'timestamp')
        location_date[_date] = [
            {
                'lat': q['latlong'].coords[0],
                'long': q['latlong'].coords[1],
                'timestamp':q['timestamp']
            } for q in location_by_date]
        location_date_list.append(location_date)


def get_case_location(case, date_from=None, date_to=None):
    """Get case location."""
    location_data = Location.objects.filter(
        case=case, active=True).exclude(
        location_locationdetails__address='N/A').order_by('timestamp').distinct('timestamp')
    if date_from and date_to:
        location_list = location_data.filter(
            timestamp__date__gte=date_from, timestamp__date__lte=date_to).values(
            'latlong', 'timestamp', 'id', 'location_locationdetails__country',
            'location_locationdetails__address', 'location_locationdetails__place',
            'location_locationdetails__locality', 'location_locationdetails__neighborhood',
            'location_locationdetails__region')
    else:
        location_list = location_data.filter(
            case=case).values(
            'latlong', 'timestamp', 'id', 'location_locationdetails__country',
            'location_locationdetails__address', 'location_locationdetails__place',
            'location_locationdetails__locality', 'location_locationdetails__neighborhood',
            'location_locationdetails__region')
    qualified_location = [
        {
            'lat': q['latlong'].coords[1],
            'lng': q['latlong'].coords[0],
            'id': q['id'],
            'timestamp':q['timestamp'],
            'place': q['location_locationdetails__place'],
            'address': q['location_locationdetails__address'],
            'locality': q['location_locationdetails__locality']
        } for q in location_list]
    return qualified_location


def get_dashboard_infor(case):
    sms = Message.objects.filter(case=case).count()
    calls = CallLog.objects.filter(case=case).count()
    location = Location.objects.filter(case=case).count()

    return sms, calls, location


def get_location_timeline(
    case_id, location_id, loc_upper_bound, loc_lower_bound):
    sent_msgs = Message.objects.filter(
        case=case_id, date_sent__gte=loc_lower_bound,
        date_sent__lte=loc_upper_bound,
        type__isnull=False).values('date_sent', 'recipient', 'type')

    received_msgs = Message.objects.filter(
        case=case_id, date_received__gte=loc_lower_bound,
        date_received__lte=loc_upper_bound,
        type__isnull=False).values('date_received', 'sender', 'type')

    outgoing_calls = CallLog.objects.filter(
        ctype='outgoing', case=case_id, date_called__gte=loc_lower_bound,
        date_called__lte=loc_lower_bound).values(
            'ctype', 'cfrom', 'cduration', 'date_called')

    incoming_calls = CallLog.objects.filter(
        ctype='incoming', case=case_id, date_called__gte=loc_lower_bound,
        date_called__lte=loc_lower_bound).values(
            'ctype', 'cfrom', 'cduration', 'date_called')

    # incoming_calls = [
    #     {'cduration': '244',
    #       'cfrom': '5713083236',
    #       'date_called': datetime.datetime(2012, 7, 6, 15, 18, 50)},
    #      {'cduration': None,
    #       'cfrom': '5712458517',
    #       'date_called': datetime.datetime(2012, 6, 22, 17, 34, 26)},
    #      {'cduration': '56',
    #       'cfrom': '7038296191',
    #       'date_called': datetime.datetime(2012, 6, 12, 20, 52, 14)},
    #      {'cduration': '20',
    #       'cfrom': '6508870260',
    #       'date_called': datetime.datetime(2012, 6, 12, 20, 4, 50)}
    #   ]
    # received_msgs = [
    #     {
    #         'sender': '5713083236',
    #         'date_received': datetime.datetime(2012, 6, 22, 17, 34, 26)
    #     }
    #  ]

    location_timeline = {
        'messages': list(received_msgs) + list(sent_msgs),
        'incoming_calls': incoming_calls
    }
    return location_timeline


def get_all_received_sms(case, date_received):
    [
        {
            'user': '+23183773',
            'sms': [
                {
                    'body': 'Hey There',
                    'date_received': '2012-08-02'
                },
                {
                    'body': 'Hey There',
                    'date_received': '2012-08-02'
                }
            ]
        },
        {
            'user': '+23183773',
            'sms': [
                {
                    'body': 'Hey There',
                    'date_received': '2012-08-02'
                },
                {
                    'body': 'Hey There',
                    'date_received': '2012-08-02'
                }
            ]
        }
    ]
    received_sms = Message.objects.filter(
        case=case, date_received__date=date_received).values_list('sender', flat=True)

    all_unique_users = list(set(list(received_sms)))
    _all_received_sms = []
    for all_unique_user in all_unique_users:
        single_user_sms = {}
        _sender = all_unique_user
        all_sms = Message.objects.filter(
            case=case, date_received__date=date_received,
            sender=all_unique_user).values('body', 'date_received')
        single_user_sms = {
            'user': _sender,
            'sms': list(all_sms)
        }
        _all_received_sms.append(single_user_sms)

    return _all_received_sms


def get_all_sent_sms(case, date_sent):
    [
        {
            'user': '+23183773',
            'sms': [
                {
                    'body': 'Hey There',
                    'date_sent': '2012-08-02'
                },
                {
                    'body': 'Hey There',
                    'date_sent': '2012-08-02'
                }
            ]
        },
        {
            'user': '+23183773',
            'sms': [
                {
                    'body': 'Hey There',
                    'date_sent': '2012-08-02'
                },
                {
                    'body': 'Hey There',
                    'date_sent': '2012-08-02'
                }
            ]
        }
    ]
    sent_sms = Message.objects.filter(
        case=case, date_sent__date=date_sent).values_list('recipient', flat=True)

    all_unique_users = list(set(list(sent_sms)))
    _all_sent_sms = []
    for all_unique_user in all_unique_users:
        single_user_sms = {}
        _recipient = all_unique_user
        all_sms = Message.objects.filter(
            case=case, date_sent__date=date_sent,
            recipient=all_unique_user).values('body', 'date_sent')
        single_user_sms = {
            'user': _recipient,
            'sms': list(all_sms)
        }
        _all_sent_sms.append(single_user_sms)

    return _all_sent_sms

def get_case_count():
    all_cases = CaseFile.objects.count()
    android_cases = CaseFile.objects.filter(platform='ANDROID').count()
    iphone_cases = CaseFile.objects.filter(platform='IOS').count()

    return {
        'total_cases': all_cases,
        'android_cases': android_cases,
        'iphone_cases': iphone_cases
    }
