"""ICMPMonitor module."""

from threading import (
    Thread
)

from sqlalchemy.orm import (
    sessionmaker
)

from argux_server.rest.client import RESTClient

class AbstractMonitor(Thread):

    """AbstractMonitor class.

    Abstract Monitor class for all monitor threads.
    """

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
        """Run placeholder."""
        raise NotImplementedError

    # pylint: disable=no-self-use
    def stop(self):
        """Stop placeholder."""
        return

    @classmethod
    def validate_options(cls, options):
        raise NotImplementedError
