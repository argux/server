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

    def run(self):
        """Run the TriggerMonitor.

        Ignores the 'interval' option at the moment.
        Trigger checks are executed at 60second intervals.
        """

        time.sleep(10)
        self.client.login()

        # Thread body.
        while True:

            try:
                self.client.evaluate_triggers()
            except HTTPError as err:
                # If a status_code is 403, try to login again
                if err.response.status_code == 403:
                    self.client.login()

            try:
                time.sleep(10)
            except KeyboardInterrupt:
                self.stop()

    @staticmethod
    def validate_options(options):
        if not 'interval' in options:
            return False

        return True
