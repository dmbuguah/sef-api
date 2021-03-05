CALL_XML_PATH = '{https://github.com/ngash/dfxml/mobile}call'
SMS_XML_PATH = '{https://github.com/ngash/dfxml/mobile}sms_mms'
METADATA_XML_PATH = '{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}metadata'
CREATOR_XML_PATH = '{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}creator'
RUSAGE_XML_PATH = '{http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML}rusage'
LOCATION_XML_PATH = '{https://github.com/ngash/dfxml/mobile}location'

CALL_NS = {
    'from': 'https://github.com/ngash/dfxml/mobile',
    'date_called': 'https://github.com/ngash/dfxml/mobile',
    'country_code': 'https://github.com/ngash/dfxml/mobile',
    'type': 'https://github.com/ngash/dfxml/mobile',
    'duration': 'https://github.com/ngash/dfxml/mobile'
}

SMS_NS = {
    'kind': 'https://github.com/ngash/dfxml/mobile',
    'recipient': 'https://github.com/ngash/dfxml/mobile',
    'body': 'https://github.com/ngash/dfxml/mobile',
    'date_sent': 'https://github.com/ngash/dfxml/mobile',
    'date_received': 'https://github.com/ngash/dfxml/mobile',
    'read': 'https://github.com/ngash/dfxml/mobile',
    'type': 'https://github.com/ngash/dfxml/mobile',
    'sender': 'https://github.com/ngash/dfxml/mobile',
    'date_received': 'https://github.com/ngash/dfxml/mobile',
    'country_code': 'https://github.com/ngash/dfxml/mobile',
}

LOCATION_NS = {
    'long': 'https://github.com/ngash/dfxml/mobile',
    'lat': 'https://github.com/ngash/dfxml/mobile',
    'source': 'https://github.com/ngash/dfxml/mobile',
    'confidence': 'https://github.com/ngash/dfxml/mobile',
    'timestamp': 'https://github.com/ngash/dfxml/mobile',
    'wifi_mac': 'https://github.com/ngash/dfxml/mobile'
}

RUSAGE_NS = {
    'utime': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'stime': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'maxrss': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'minflt': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'majflt': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'nswap': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'inblock': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'oublock': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML',
    'clocktime': 'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML'
}
