"""DNSMonitorDomain."""

from sqlalchemy import (
    Column,
    ForeignKey,
    Index,
    Integer,
    Boolean,
    Text,
)

from sqlalchemy.orm import (
    relationship,
    backref
)

from . import BASE

from .Monitor import Monitor


# pylint: disable=too-few-public-methods
class DNSMonitorDomain(BASE):

    """DNSMonitorDomain Class.

    Base object for referencing DNSMonitorDomains.
    """

    __tablename__ = 'dns_monitor_domain'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    monitor_id = Column(Integer, ForeignKey('monitor.id'), nullable=False)
    monitor = relationship(
        Monitor,
        backref=backref(
            'domains',
            cascade='save-update, merge, delete'
        )
    )
    domain = Column(Text, nullable=False)
    record_a = Column(Boolean, nullable=False)
    record_aaaa = Column(Boolean, nullable=False)
    record_mx = Column(Boolean, nullable=False)

Index(
    'u_dns_monitor_domain_id_index',
    DNSMonitorDomain.id,
    unique=True)
Index(
    'u_dns_monitor_domain_name_id_index',
    DNSMonitorDomain.domain,
    DNSMonitorDomain.monitor_id,
    unique=True)
