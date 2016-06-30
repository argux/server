"""ArguxServer Data Access Objects."""

from .ItemDAO import ItemDAO
from .HostDAO import HostDAO
from .NoteDAO import NoteDAO
from .UserDAO import UserDAO
from .TriggerDAO import TriggerDAO
from .MonitorDAO import MonitorDAO
from .GraphDAO import GraphDAO


# pylint: disable=too-few-public-methods
class DAO(object):

    """Main DAO Class.

    This Class loads all modules containg the other DAO functions.
    """

    def __init__(self, db_session):
        """Constructor function.

        Initialises public member DAO modules.
        """
        self.db_session = db_session

        self.host_dao = HostDAO(db_session)
        self.item_dao = ItemDAO(db_session)
        self.note_dao = NoteDAO(db_session)
        self.user_dao = UserDAO(db_session)
        self.trigger_dao = TriggerDAO(db_session)
        self.monitor_dao = MonitorDAO(db_session)
        self.graph_dao = GraphDAO(db_session)

    def get_active_alert_count(self, host):
        d_items = self.item_dao.get_items_from_host(host)
        if (d_items == None):
            return 0

        n_total_alerts = 0

        for item in d_items:
            n_alerts = self.item_dao.get_active_alert_count(item)
            n_total_alerts += n_alerts

        return n_total_alerts
