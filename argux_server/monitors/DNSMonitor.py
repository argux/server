"""DNSMonitor module."""

import time
import logging

import re
import subprocess
from subprocess import CalledProcessError

import shutil
import os

from datetime import datetime

from .ExternalMonitor import ExternalMonitor


def parse_dig(output):
    """Parse dig output.

    (python3.3)[stephan@hermes net-monitor]$ dig @server +noall +answer -t A example.com
    """

    logger = logging.getLogger(__name__)

    ret_val = []

    for row in output.split('\n'):
        match = re.search(
            '^(?P<name>[^ \t]+)[ \t]+'+
            '(?:(?P<ttl>[0-9]+)[ \t]+)?'+
            '(?P<in>[^ \t]+)[ \t]+'+
            '(?P<type>[^ \t]+)[ \t]+'+
            '(?:(?P<prio>[0-9]+)[ \t]+)?'+
            '(?P<value>[^ ]+)', row)

        if match:
            ret_val.append({
                'name': match.group('name'),
                'ttl': match.group('ttl'),
                'in': match.group('in'),
                'type': match.group('type'),
                'value': match.group('value'),
                'prio': match.group('prio')
                })

    return ret_val

DIG = 'dig @{address} +noall +answer -t {_type} {domain}'

PARSE = parse_dig

class DNSMonitor(ExternalMonitor):

    """DNSMonitor class.

    Queries Monitor schedules monitoring actions.
    """

    def __init__(self, settings):
        """Initialise DNSMonitor.
        """

        super(DNSMonitor, self).__init__(settings)
        self.monitor_type = 'dns'

    @staticmethod
    def validate_options(options):
        if 'interval' not in options:
            raise ValueError

        return True

    # pylint: disable=no-self-use
    def monitor_once(self, client, monitor):
        """
        Monitor once.
        """

        domain = None

        domains = client.get_dns_domains(
            monitor['host'],
            monitor['address'])

        if (shutil.which('dig') == None):
            self.logger.warn("dig command could not be found, skipping...")
            return

        for domain in domains:
            if domain['record_a']:
                self.check_dns(client, monitor, 'A', domain['domain'])
            if domain['record_aaaa']:
                self.check_dns(client, monitor, 'AAAA', domain['domain'])
            if domain['record_mx']:
                self.check_dns(client, monitor, 'MX', domain['domain'])

        return

    def check_dns(self, client, monitor, _type, domain):
        """
        Check DNS record
        """
        timestamp = datetime.now()
        values = []

        address = monitor['address']
        host = monitor['host']

        dig_cmd = DIG.format(
            address=address,
            _type=_type,
            domain=domain)

        try:
            output = subprocess.check_output(
                dig_cmd, shell=True, universal_newlines=True)
            values = PARSE(output)
        except CalledProcessError as err:
            self.logger.warn('warning: '+str(err))
        except Exception as err:
            self.logger.error('error: '+str(err))

        for index, value in enumerate(
                sorted(
                    values,
                    key=lambda value: value['value']
                )
            ):

            val_item_key = 'dns.record[type='+_type+',domain='+domain+',idx='+str(index)+']'
            params = {
                'name': 'DNS '+_type+' record ('+str(index)+') for '+domain,
                'type': 'text',
                'category': 'Network',
                'unit': None,
                'description': 'DNS record information',
            }

            client.create_item(
                host,
                val_item_key,
                params)

            if value['value'] is not None:
                client.push_value(
                    host,
                    val_item_key,
                    timestamp,
                    value['value'])
