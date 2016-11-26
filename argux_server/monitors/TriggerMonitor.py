"""TriggerMonitor module."""

import time
import platform

import re
import subprocess

from requests.exceptions import (
    HTTPError
)

from datetime import datetime

from .AbstractMonitor import AbstractMonitor

from argux_server.rest.client import (
    RESTClient,
)


class TriggerMonitor(AbstractMonitor):

    """TriggerMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def process_monitor(self):
        """Run the TriggerMonitor.

        Ignores the 'interval' option at the moment.
        Trigger checks are executed at 60second intervals.
        """
        try:
            self.client.evaluate_triggers()
        except HTTPError as err:
            pass

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            return False

        return True
