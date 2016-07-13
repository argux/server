"""ArguxServer Data Access Objects."""

from argux_server.models import (
    Host,
    Item,
    TriggerSeverity
)

from argux_server.dao.util import (
    TRIGGER_CLASS,
    ALERT_CLASS
)

from .ItemDAO import ItemDAO
from .HostDAO import HostDAO
from .NavDAO import NavDAO
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
        self.nav_dao = NavDAO(db_session)
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

    def get_host_severity(self, host):
        """Return highest severity of active triggers for this host.

        This should be optimized... running x queries for each individual
        host that needs it is very slow. - Want to use UNION, but
        I couldn't get it working with SQLAlchemy.
        """

        existing_query = None
        max_severity_level = -1
        max_severity = None

        for key in TRIGGER_CLASS:
            trigger_klass = TRIGGER_CLASS.get(key)
            alert_klass = ALERT_CLASS.get(key)

            severity = self.db_session.query(TriggerSeverity)\
                .filter(TriggerSeverity.id.in_(
                    self.db_session.query(trigger_klass.severity_id)\
                    .filter(trigger_klass.item_id.in_(
                        self.db_session.query(Item.id)
                        .filter(Item.host_id == host.id)
                    ))\
                    .filter(trigger_klass.id.in_(
                        self.db_session.query(alert_klass.trigger_id)
                        .filter(alert_klass.end_time.is_(None))
                    ))
                ))\
                .order_by(TriggerSeverity.level.desc())\
                .first()
            if severity is not None:
                if severity.level > max_severity_level:
                    max_severity_level = severity.level
                    max_severity = severity

        return max_severity

