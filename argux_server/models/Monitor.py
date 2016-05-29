"""Monitor Module, containing Monitor model."""

from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    ForeignKey,
    DateTime,
    Boolean
)

from sqlalchemy.orm import (
    relationship
)

from .HostAddress import HostAddress
from .MonitorType import MonitorType

from . import BASE

# pylint: disable=too-few-public-methods
class Monitor(BASE):

    """
    Monitor class.

    Model for storing monitors.
    """

    __tablename__ = 'monitor'
    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    host_address_id = Column(Integer, ForeignKey('host_address.id'), nullable=False)
    host_address = relationship('HostAddress', backref='monitors')
    monitor_type_id = Column(Integer, ForeignKey('monitor_type.id'), nullable=False)
    monitor_type = relationship('MonitorType', backref='monitors')
    active = Column(Boolean, nullable=False, default=True)
    last_run = Column(DateTime, nullable=True, default=None)


Index(
    'u_monitor_host_a_monitor_t_id',
    Monitor.monitor_type_id,
    Monitor.host_address_id,
    unique=True)
