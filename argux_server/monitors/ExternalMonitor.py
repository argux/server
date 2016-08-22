"""ICMPMonitor module."""

import time

from requests.exceptions import (
    HTTPError
)

from .AbstractMonitor import AbstractMonitor

class ExternalMonitor(AbstractMonitor):

    """ExternalMonitor class.

    Abstract class for all external monitor threads.
    """

    def __init__(self, settings):
        """Initialise ExternalMonitor.

        This constructor builds a RESTClient object to communicate with the
        rest of the server.
        """
        super(ExternalMonitor, self).__init__(settings)

    # pylint: disable=no-self-use
    def process_monitor(self):
        mons = self.client.get_monitors(self.monitor_type)
        for mon in mons:
            if mon['active']:
                try:
                    self.monitor_once(self.client, mon)
                except Exception as e:
                    print(str(e))
