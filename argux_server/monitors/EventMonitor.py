"""EventMonitor module."""

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


class EventMonitor(AbstractMonitor):

    """EventMonitor class.

    Queries Monitor dao and schedules monitoring actions.
    """

    def process_monitor(self):
        """Run the EventMonitor.

        Ignores the 'interval' option at the moment.
        Event checks are executed at 60second intervals.
        """
        print("EventMonitor")

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            return False

        return True
