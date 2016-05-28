"""DNSMonitor module."""

import time

import re
import subprocess

import shutil
import os

from datetime import datetime

from .AbstractMonitor import AbstractMonitor


def parse_dig(output):
    """Parse dig output.

    (python3.3)[stephan@hermes net-monitor]$ dig @server +noall +answer -t A example.com
    """
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

class DNSMonitor(AbstractMonitor):

    """DNSMonitor class.

    Queries Monitor schedules monitoring actions.
    """

    def run(self):
        """Run the DNSMonitor.

        Ignores the 'interval' option at the moment.
        DNS checks are executed at 300second intervals.
        """

        time.sleep(30)
        self.client.login()

        # Thread body.
        while True:
            cmd = shutil.which('dig', mode=os.X_OK)
            if cmd:
                # Only run if dig can be found
                try:
                    mons = self.client.get_monitors('dns')
                    for mon in mons:
                        if mon['active']:
                            try:
                                DNSMonitor.monitor_once(self.client, mon)
                            except Exception as err:
                                print(">> "+str(err))
                except Exception as err:
                    print("DNS Monitor Error: "+str(err))

            try:
                time.sleep(15)
            except KeyboardInterrupt:
                self.stop()

    @staticmethod
    def validate_options(options):
        if 'interval' not in options:
            raise ValueError

        return True

    @staticmethod
    def monitor_once(client, monitor):
        """
        Monitor once.
        """

        domain = None

        domains = client.get_dns_domains(
            monitor['host'],
            monitor['address'])

        for domain in domains:
            if domain['record_a']:
                DNSMonitor.check_dns(client, monitor, 'A', domain['domain'])
            if domain['record_aaaa']:
                DNSMonitor.check_dns(client, monitor, 'AAAA', domain['domain'])
            if domain['record_mx']:
                DNSMonitor.check_dns(client, monitor, 'MX', domain['domain'])

        return

    @staticmethod
    def check_dns(client, monitor, _type, domain):
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
        except Exception as err:
            print('error: '+str(err))

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
