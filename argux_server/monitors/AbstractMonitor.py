"""ICMPMonitor module."""

import time

from threading import (
    Thread
)

from requests.exceptions import (
    HTTPError
)

from sqlalchemy.orm import (
    sessionmaker
)

from argux_server.rest.client import RESTClient

class AbstractMonitor(Thread):

    """AbstractMonitor class.

    Abstract Monitor class for all monitor threads.
    """

    monitor_type = None

    def __init__(self, settings):
        """Initialise AbstractMonitor.

        This constructor builds a RESTClient object to communicate with the
        rest of the server.
        """
        super(AbstractMonitor, self).__init__()
        self.daemon = True

        self.client = RESTClient(
            'http://localhost:7000',
            '__monitor__',
            settings['monitor_pass'])

    # pylint: disable=no-self-use
    def run(self):
        """Run the Monitor.

        Ignores the 'interval' option at the moment.
        checks are executed at 60second intervals.
        """

        time.sleep(20)
        self.client.login()

        # Thread body.
        while True:
            try:
                self.process_monitor()
            except HTTPError as err:
                # If a status_code is 403, try to login again
                if err.response.status_code == 403:
                    self.client.login()
                else:
                    print("Monitor Error: "+str(e))
            except Exception as e:
                print("Monitor Error: "+str(e))

            try:
                time.sleep(60)
            except KeyboardInterrupt:
                self.stop()

    # pylint: disable=no-self-use
    def stop(self):
        """Stop placeholder."""
        return

    @classmethod
    def validate_options(cls, options):
        raise NotImplementedError

    # pylint: disable=no-self-use
    def monitor_once(self, client, monitor):
        raise NotImplementedError

    # pylint: disable=no-self-use
    def process_monitor(self, client, monitor):
        raise NotImplementedError
