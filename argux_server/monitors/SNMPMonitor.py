"""SNMPMonitor module."""

import time

import re
import subprocess

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

import transaction


class SNMPMonitor(AbstractMonitor):

    """SNMPMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def __init__(self, settings):
        """Initialise SNMPMonitor.
        """

        super(SNMPMonitor, self).__init__(settings)
        self.monitor_type = 'snmp'

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            raise KeyError

        return True

    # pylint: disable=no-self-use
    def monitor_once(self, client, monitor):
        """
        Monitor once.
        """
        system_name = platform.system()

        return
